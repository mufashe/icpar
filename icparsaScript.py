import datetime
import smtplib
import warnings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from apscheduler.schedulers.blocking import BlockingScheduler

import os
import django
import mysql.connector

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'icpars.settings')
django.setup()

configureTarget = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'icpars',
}


def sendNotification():
    print("Connecting to target database...")
    target_dataBase = mysql.connector.connect(**configureTarget)
    targetCursor = target_dataBase.cursor()
    print("Connected to target database.")

    from icparsa.models import ContractHistory
    from icparsa.models import Contract
    from icparsa.models import ContractSetting
    contractsList = Contract.objects.all()
    contractSettingsList = ContractSetting.objects.all()
    now_date = datetime.datetime.now().date()

    for contract in contractsList:
        contract.conHist = ContractHistory.objects.filter(contract=contract).count()
        if contract.signedDate and contract.expirationDate:

            difference = contract.expirationDate - now_date
            contract.days_left = difference.days
            if contract.conHist >= 3:
                print('renewal contract exceeded !')
            for cs in contractSettingsList:
                emailList = [contract.departmentUnit.email, cs.managingEmail]

                if contract.contract_status != 'CANCELED':
                    if contract.notificationSentOn is None and contract.days_left < cs.expirationDays \
                            and contract.notificationRemindingTimes == 0:
                        contract.is_expiringSoon = True
                        contract.notificationSentOn = now_date
                        contract.notificationRemindingTimes = 1
                        send_email(emailList, contract)
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


warnings.filterwarnings("ignore", category=UserWarning, module='tzlocal')
scheduler = BlockingScheduler()
# scheduler.add_job(sendNotification, 'interval', days=7)
scheduler.add_job(sendNotification, 'interval', seconds=15)
scheduler.start()
