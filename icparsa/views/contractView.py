import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib import messages
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from icparsa.decorators import allowed_users
from icparsa.forms.ContractForm import ContractForm
from icparsa.models.contractSetting import ContractSetting
from icparsa.models.models import Contract, ContractHistory
import django_excel as excel


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def recordContract(request):
    nextNumber = Contract.objects.all().count() + 1
    contractForm = ContractForm(initial={'number': nextNumber})
    if request.method == 'POST':
        contractForm = ContractForm(request.POST)
        contractForm.save()
        messages.success(request, 'Contract recorded !')
        # return redirect('conts')
    context = {'contractForm': contractForm}
    return render(request, 'icparsa/contract/contract.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def listContracts(request):
    contractsList = Contract.objects.all()
    contractSettingsList = ContractSetting.objects.all()
    now_date = datetime.datetime.now().date()
    logged_in_user = request.user
    admin = Q(groups__name='admin')
    end_user = Q(groups__name='end_user')
    procurement = Q(groups__name='procurement')

    admins = User.objects.filter(admin)
    end_users = User.objects.filter(end_user)
    procurementManager = User.objects.filter(procurement)
    for contract in contractsList:
        contract.conHist = ContractHistory.objects.filter(contract=contract).count()
        if contract.signedDate and contract.expirationDate:
            # difference = c.expirationDate - c.signedDate
            difference = contract.expirationDate - now_date
            contract.days_left = difference.days
            if contract.days_left < 0:
                contract.contract_status = 'EXPIRED'
            if contract.conHist >= 3:
                messages.error(request, 'renewal contract exceeded !')
            for cs in contractSettingsList:
                emailList = [contract.departmentUnit.email, cs.managingEmail]
                # if c.contractType == cs.type:
                if contract.contract_status != 'CANCELED':
                    if contract.notificationSentOn is None and contract.days_left < cs.expirationDays \
                            and contract.notificationRemindingTimes == 0:
                        contract.is_expiringSoon = True
                        contract.notificationSentOn = now_date
                        contract.notificationRemindingTimes = 1
                        # send_email(emailList, contract)
                        print("send notification email")
                    elif contract.notificationSentOn and (
                            now_date - contract.notificationSentOn).days > cs.notificationsDaysToWait and \
                            contract.notificationRemindingTimes < cs.remindingTimes:
                        print(f'Before incrementing: {contract.notificationRemindingTimes}')
                        contract.notificationSentOn = now_date
                        contract.notificationRemindingTimes += 1
                        print(f'After incrementing: {contract.notificationRemindingTimes}')
                        # send_email(emailList, contract)
                        print("send notification email")

        else:
            contract.days_left = None
        contract.save()

    context = {'contractsList': contractsList, 'conset': contractSettingsList, 'loggedInUser': logged_in_user,
               'admins': admins, 'end_users': end_users, 'procurementManager': procurementManager}
    return render(request, 'icparsa/contract/contracts.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def updateContract(request, pk):
    cont = Contract.objects.get(id=pk)
    contractForm = ContractForm(instance=cont)
    if request.method == 'POST':
        contractForm = ContractForm(request.POST, instance=cont)
        if contractForm.is_valid():
            contractForm.save()
            return redirect('conts')
    context = {'contractForm': contractForm, 'cont': cont}
    return render(request, 'icparsa/contract/contract.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def deleteContract(request, pk):
    cont = Contract.objects.get(id=pk)
    if request.method == 'POST':
        cont.delete()
        return redirect('/conts')
    context = {'cont': cont}
    return render(request, 'icparsa/contract/delContract.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def searchWithDates(request):
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    contractsList = Contract.objects.all()
    if fromDate and toDate:
        from_Date = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
        to_Date = datetime.datetime.strptime(toDate, '%Y-%m-%d')

        contractsList = contractsList.filter(Q(signedDate__gte=from_Date) & Q(signedDate__lte=to_Date))
        context = {'contractsList': contractsList}
        return render(request, 'icparsa/contract/contracts.html', context)
    else:
        return render(request, 'icparsa/contract/contracts.html')


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def searchCompanyName(request):
    shaka = request.GET.get('shaka', '')
    if shaka:
        contractList = Contract.objects.filter(Q(secondParty__name__icontains=shaka) | Q(name__icontains=shaka))
    else:
        contractList = Contract.objects.none()
    context = {'contractsList': contractList, 'shaka': shaka}
    return render(request, 'icparsa/contract/contracts.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def updateContractStatus(request, pk):
    contract = Contract.objects.get(id=pk)
    if contract is not None:

        if contract.contract_status == 'SIGNED':
            contract.contract_status = 'CANCELED'
        else:
            contract.contract_status = 'SIGNED'
        contract.save()
        return redirect('/conts')
    context = {'contractList': contract}
    return render(request, 'icparsa/contract/contracts.html', context)


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def exportContractExport(request):
    contractList = Contract.objects.all()
    columnToExport = [field.name for field in Contract._meta.get_fields()]
    response = excel.make_response_from_query_sets(contractList, columnToExport, 'csv', file_name='Contract_List')
    return response


@allowed_users(allowed_roles=['procurement', 'admin'])
@login_required(login_url='log')
def contractRenew(request, pk):
    contract = get_object_or_404(Contract, id=pk)
    contractForm = ContractForm(instance=contract)
    renewalTimes = ContractHistory.objects.filter(contract=contract).count()

    for field in contractForm.fields:
        if field not in ['signedDate', 'expirationDate', 'description']:
            contractForm.fields[field].widget.attrs['readonly'] = True

    if request.method == 'POST':
        contractForm = ContractForm(request.POST, instance=contract)
        if contractForm.is_valid():
            ContractHistory.objects.create(
                contract=contract,
                signedDate=contract.signedDate,
                expirationDate=contract.expirationDate,
                renewDate=timezone.now(),
                renewalCounter=renewalTimes + 1
            )
            contract.contract_status = 'SIGNED'
            contractForm.save()
            return redirect('conts')
    context = {'contractList': contract, 'contractForm': contractForm}
    return render(request, 'icparsa/contract/contract.html', context)


def contractRenewalHistory(request, pk):
    contract = get_object_or_404(Contract, id=pk)
    renewalReport = ContractHistory.objects.filter(contract=contract)
    context = {'renewalReport': renewalReport, 'contract': contract}
    return render(request, 'icparsa/contract/contracts.html', context)


def send_email(recipient_email, contract):
    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp_server.starttls()
    sender_email = 'mufasheonline@gmail.com'
    password = 'jemy yorr xgnp ihdk'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    # msg['To'] = recipient_email
    msg['To'] = ','.join(recipient_email)
    msg['Subject'] = 'Contract Expiration Notification'

    # body = 'Testing send email to notify the expiration of contract'

    body = f""" <html> <body> <p>Hello,</p> <p>This is a notification about the following contract:</p> <table
    style="border-collapse: collapse; width: 100%;"> <tr><td style="border: 1px solid black; padding:
    5px;">Name:</td><td style="border: 1px solid black; padding: 5px;">{contract.name}</td></tr> <tr><td
    style="border: 1px solid black; padding: 5px;">Contract Type:</td><td style="border: 1px solid black; padding:
    5px;">{contract.contractType}</td></tr> <tr><td style="border: 1px solid black; padding: 5px;">Contract
    Status:</td><td style="border: 1px solid black; padding: 5px;">{contract.contract_status}</td></tr> <tr><td
    style="border: 1px solid black; padding: 5px;">Second Party:</td><td style="border: 1px solid black; padding:
    5px;">{contract.secondParty}</td></tr> <tr><td style="border: 1px solid black; padding: 5px;">Signed
    Date:</td><td style="border: 1px solid black; padding: 5px;">{contract.signedDate}</td></tr> <tr><td
    style="border: 1px solid black; padding: 5px;">Expiration Date:</td><td style="border: 1px solid black; padding:
    5px;">{contract.expirationDate}</td></tr> <tr style="background-color: #fc6b0d"><td style="border: 1px solid
    black; padding: 5px;">Days Left:</td><td style="border: 1px solid black; padding: 5px;">
    {contract.days_left}</td></tr>
        </table>
        <p>Please take the necessary actions.</p>
        <p>Best regards,</p>

    </body>
    </html>

    """
    msg.attach(MIMEText(body, 'html'))
    try:
        smtp_server.login(sender_email, password)
        print("Login succeed")
        contract.notificationSentOn = datetime.datetime.now().date()
        contract.save()
        smtp_server.send_message(msg)
        print("Email Sent Successfully")

    except Exception as e:
        print(f"Failed to send email : {str(e)}")
        print("Login Failed")
