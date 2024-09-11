import base64
import io
import json
import tempfile
from datetime import date

import requests
from PIL import UnidentifiedImageError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Q
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer, Paragraph
from PIL import Image as PILImage, UnidentifiedImageError

from company.models import CompanyEmployee, Department, Title, EmployeeAsUserSignature, Unit
from icparsa.decorators import allowed_users
from leaveMan.forms.leaveForm import LeaveForm
from leaveMan.forms.signaturePasswordForm import SignaturePasswordForm
from leaveMan.models import Leave, LeaveDecision
from io import BytesIO


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin', 'leaveManager'])
@login_required(login_url='log')
def recordLeave(request):
    next_number = Leave.objects.all().count() + 1
    empForm = LeaveForm(initial={'number': next_number})
    if request.method == 'POST':
        empForm = LeaveForm(request.POST)
        empForm.save()
        return redirect('lil')

    context = {'empForm': empForm}
    return render(request, 'leaveMan/leave/leave.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin', 'leaveManager', 'director', 'manager'])
def listLeave(request):
    leaveDecisionMakersGroup = Q(groups__name='leaveDecisionMakers')
    adminsGroup = Q(groups__name='admin')
    leaveDecisionMakersMember = User.objects.filter(leaveDecisionMakersGroup)
    adminsGroupMember = User.objects.filter(adminsGroup)

    leaveDecisions = {ld.leave.id: ld.decisionStatus for ld in
                      LeaveDecision.objects.filter(approvingEmployee=request.user)}
    user_role = request.user.groups.first().name

    user_employee = CompanyEmployee.objects.get(email=request.user.email)

    employee_title = user_employee.title.name.lower() if user_employee.title else ''

    if 'manager' in employee_title:
        leaveList = Leave.objects.filter(
            models.Q(employee__title__unit=user_employee.title.unit) |
            models.Q(employee__title__name__icontains='manager',
                     employee__department=user_employee.department)).order_by('number')

    elif 'director' in employee_title:
        leaveList = Leave.objects.filter(
            Q(employee__department=user_employee.department) |
            Q(employee__title__name__icontains='director')).order_by('number')

    elif 'admin' in employee_title:
        leaveList = Leave.objects.all().order_by('number')

    elif 'ceo' in employee_title:
        leaveList = Leave.objects.all().order_by('number')

    else:
        leaveList = Leave.objects.none()

    context = {'leaveList': leaveList, 'leaveDecisionMakersMember': leaveDecisionMakersMember,
               'adminsGroupMember': adminsGroupMember, 'leaveDecisions': leaveDecisions}
    return render(request, 'leaveMan/leave/leaveList.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin', 'leaveManager'])
def updateLeave(request, pk):
    leave = Leave.objects.get(id=pk)
    leaveForm = LeaveForm(instance=leave)
    if request.method == 'POST':
        leaveForm = LeaveForm(request.POST, instance=leave)
        if leaveForm.is_valid():
            leaveForm.save()
            return redirect('lil')
    context = {'empForm': leaveForm}
    return render(request, 'leaveMan/leave/leave.html', context)


def updateLeaveStatus(request, pk):
    leaveId = request.POST.get('leave_id')
    signaturePassword = request.POST.get('password')
    leave = get_object_or_404(Leave, id=leaveId)
    userSignature = get_object_or_404(EmployeeAsUserSignature, employee=request.user)

    if check_password(signaturePassword, userSignature.signature_password):
        if leave.leave_status == 'PENDING':
            leave.leave_status = 'APPROVED'
        elif leave.leave_status == 'APPROVED':
            leave.leave_status = 'DENIED'
        else:
            leave.leave_status = 'PENDING'

        leave.save()

        existingLeaveDecision = LeaveDecision.objects.filter(
            leave=leave,
            approvingEmployee=request.user,
        ).first()

        if existingLeaveDecision:
            existingLeaveDecision.decisionStatus = leave.leave_status
            existingLeaveDecision.signature = userSignature
            existingLeaveDecision.save()

        else:
            newDecision = LeaveDecision.objects.create(
                leave=leave,
                requestingEmployee=leave.employee,
                approvingEmployee=request.user,
                decisionStatus=leave.leave_status,
                signature=userSignature,
            )
            newDecision.save()
        if 'Manager' not in leave.employee.title.name and 'Director' not in leave.employee.title.name:
            manager = get_object_or_404(CompanyEmployee, department=leave.employee.department,
                                        title__name__icontains='Manager')
            director = get_object_or_404(CompanyEmployee, department=leave.employee.department,
                                         title__name__icontains='Director')
            managerSignature = get_object_or_404(EmployeeAsUserSignature, employee=manager)
            directorSignature = get_object_or_404(EmployeeAsUserSignature, employee=director)

            LeaveDecision.objects.get_or_create(
                leave=leave,
                requestingEmployee=leave.employee,
                approvingEmployee=request.user,
                defaults={'decisionStatus': 'PENDING', 'signature': managerSignature}
            )

            LeaveDecision.objects.get_or_create(
                leave=leave,
                requestingEmployee=leave.employee,
                approvingEmployee=request.user,
                defaults={'decisionStatus': 'PENDING', 'signature': directorSignature}
            )
        elif 'Manager' in leave.employee.title.name:
            director = get_object_or_404(CompanyEmployee, department=leave.employee.department, title__name='Director')
            directorSignature = get_object_or_404(EmployeeAsUserSignature, employee=director)

            LeaveDecision.objects.get_or_create(
                leave=leave,
                requestingEmployee=leave.employee,
                approvingEmployee=request.user,
                defaults={'decisionStatus': 'PENDING', 'signature': directorSignature}
            )

        return JsonResponse({'success': True, 'new_status': leave.leave_status})
    else:
        return JsonResponse({'success': False, 'error': 'Incorrect password'})


@login_required(login_url='log')
# @allowed_users(allowed_roles=['admin', 'leaveManager', 'end_user'])
def give_leave(request, pk):
    emp = get_object_or_404(CompanyEmployee, id=pk)
    next_number = Leave.objects.all().count() + 1
    if request.method == 'POST':
        leaveForm = LeaveForm(request.POST)
        if leaveForm.is_valid():
            leave = leaveForm.save(commit=False)
            leave.employee = emp
            leave.first_name = emp.first_name
            leave.last_name = emp.last_name
            leave.birth_date = emp.birth_date
            # leave.department = employee.department
            leave.department = Department.objects.get(name=emp.department)
            leave.title = emp.title
            leave.hire_date = emp.hire_date
            leave.home_phone = emp.home_phone
            leave.mobile_phone = emp.mobile_phone
            leave.home_address = emp.home_address
            leave.months_in_institution = (date.today() - emp.hire_date).days // 30
            conflictedLeaves = Leave.objects.filter(Q(employee__department=emp.department),
                                                    Q(outDate__lte=leave.inDate, inDate__gte=leave.outDate))

            if conflictedLeaves.exists():
                messages.error(request, 'Department allow only one employee at time')
                return redirect('lem')
            leave.save()

            userSignature = get_object_or_404(EmployeeAsUserSignature, employee=request.user)
            LeaveDecision.objects.create(
                leave=leave,
                requestingEmployee=leave.employee,
                approvingEmployee=request.user,
                decisionStatus='REQUESTING',
                signature=userSignature
            )

            if 'Manager' not in emp.title.name and 'Director' not in emp.title.name:
                manager = get_object_or_404(CompanyEmployee, department=emp.department,
                                            title__name__icontains='Manager')
                director = get_object_or_404(CompanyEmployee, department=emp.department,
                                             title__name__icontains='Director')
                managerSignature = get_object_or_404(EmployeeAsUserSignature, employee=manager)
                directorSignature = get_object_or_404(EmployeeAsUserSignature, employee=director)

                LeaveDecision.objects.create(
                    leave=leave,
                    requestingEmployee=emp,
                    approvingEmployee=request.user,
                    decisionStatus='REQUESTING',
                    signature=managerSignature,

                )

                LeaveDecision.objects.create(
                    leave=leave,
                    requestingEmployee=emp,
                    approvingEmployee=request.user,
                    decisionStatus='REQUESTING',
                    signature=directorSignature
                )
            elif emp.title == 'Manager':
                director = get_object_or_404(CompanyEmployee, department=emp.department,
                                             title__name__icontains='Director')
                directorSignature = get_object_or_404(EmployeeAsUserSignature, employee=director)

                LeaveDecision.objects.create(
                    leave=leave,
                    requestingEmployee=emp,
                    approvingEmployee=request.user,
                    decisionStatus='REQUESTING',
                    signature=directorSignature
                )

            messages.success(request, 'Leave Request Sent Please wait for Approval')
            # return redirect('lem')
        else:
            print(leaveForm.errors)
    else:
        annual_leave_days = 18
        months_in_institution = (date.today() - emp.hire_date).days // 30
        total_leave_days = int((annual_leave_days / 12) * months_in_institution)

        # usedLeaveDays = Leave.objects.filter(first_name=emp.first_name, last_name=emp.last_name).aggregate(
        #     Sum('leave_days_used')).get('leave_days_used__sum', 0)

        usedLeaveDays = Leave.objects.filter(employee=emp).aggregate(Sum('leave_days')) \
            .get('leave_days__sum', 0)
        if usedLeaveDays is None:
            usedLeaveDays = 0
        print("**********************USED LEAVE DAYS******************", usedLeaveDays)
        print("Unit", emp.title)
        initial_data = {
            'number': next_number,
            'first_name': emp.first_name,
            'last_name': emp.last_name,
            'hire_date': emp.hire_date,
            'home_phone': emp.home_phone,
            'mobile_phone': emp.mobile_phone,
            'home_address': emp.home_address,
            'birth_date': emp.birth_date,
            'months_in_institution': months_in_institution,
            'total_leave_days': total_leave_days,
            'leave_days_used': usedLeaveDays,
            'title': emp.title,
            'department': emp.department
        }
        print("Initial data:", initial_data)
        leaveForm = LeaveForm(initial=initial_data)
        # leaveForm = LeaveForm()

    ongoingLeaves = Leave.objects.filter(employee__department=emp.department, leave_status__iexact='Pending')

    context = {'empForm': leaveForm, 'ongoingLeaves': ongoingLeaves}
    return render(request, 'leaveMan/leave/leave.html', context)


@login_required(login_url='log')
@allowed_users(allowed_roles=['admin', 'leaveManager'])
def loadTitle(request):
    department_id = request.GET.get('department_id')
    title = Title.objects.filter(department_id=department_id)
    context = {'title': title}
    return render(request, 'leaveMan/leave/titleDropDown.html', context)


def get_public_holidays(country, year, api_key):
    api_url = f'https://api.api-ninjas.com/v1/holidays?country={country}&year={year}'
    response = requests.get(api_url, headers={'X-Api-Key': api_key})
    if response.status_code == requests.codes.ok:
        try:
            holidays = response.json()
            # Extract the dates of the holidays
            holiday_dates = [holiday['date'] for holiday in holidays]
            return holiday_dates
        except json.JSONDecodeError:
            return 'Error decoding JSON'
    else:
        return f'Error: {response.status_code}, {response.text}'


def holidays_view(request, country):
    api_key = '38etVRVE5Rmf3vIvphOJ2w==jo00VBVefQQvJj92'  # replace with your actual API key
    year = 2025
    country = 'rw'
    holidays = get_public_holidays(country, year, api_key)
    return JsonResponse(holidays, safe=False)


def publicHolidaysAPICaller(request, country, year):
    api_key = '38etVRVE5Rmf3vIvphOJ2w==jo00VBVefQQvJj92'  # replace with your actual API key
    holidays = get_public_holidays(country, year, api_key)
    return JsonResponse(holidays, safe=False)


pdfmetrics.registerFont(
    TTFont('Tahoma', 'D:/Projects/ICPAR/icpars/static/fonts/tahoma.ttf'))


def generateLeave(request, pk):
    leave = get_object_or_404(Leave, id=pk)
    buffer = io.BytesIO()
    document = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=1 * inch, rightMargin=1 * inch)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Tahoma', fontName='Tahoma', fontSize=10))

    data = [
        ["Names", f"{leave.employee.first_name} {leave.employee.last_name}"],
        ["Phone", leave.employee.mobile_phone],
        ["Department", leave.employee.department.name],
        ["Title", leave.employee.title.name],
        ["Contract Information", ""],  # New row to span all columns
        ["Hired Date", leave.employee.hire_date],
        ["Months in Institution", leave.months_in_institution],
        ["Total Leave Days", leave.total_leave_days],
        ["Leave Days Used", leave.leave_days_used],
        ["Leave Information", ""],
        ["Leave Days", leave.leave_days],
        ["Leave Period", f"From: {str(leave.outDate)}"],  # Leave Period spans two rows
        ["", f"To: {str(leave.inDate)}"],
    ]

    table = Table(data, colWidths=[2.5 * inch, 5.5 * inch])

    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Tahoma'),  # Use registered Tahoma font here
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Increase font size to 12
        ('BACKGROUND', (0, 0), (-1, 0), colors.skyblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('SPAN', (0, 4), (-1, 4)),  # Span Contract Information row
        ('ALIGN', (0, 4), (-1, 4), 'CENTER'),
        ('BACKGROUND', (0, 4), (-1, 4), colors.skyblue),
        ('SPAN', (0, 9), (-1, 9)),  # Span Leave Information row
        ('ALIGN', (0, 9), (-1, 9), 'CENTER'),
        ('BACKGROUND', (0, 9), (-1, 9), colors.skyblue),
        ('SPAN', (0, 11), (0, 12)),  # Span Leave Period column
    ]))

    elements = []

    # Add logo and header in a combined table
    logo_path = "static/img/ICPAR Logo.png"  # Update with the path to your logo image
    logo_image = Image(logo_path)
    logo_image.drawHeight = 1 * inch  # Adjust height as needed
    logo_image.drawWidth = 1 * inch  # Adjust width as needed

    header_data = [[logo_image, Paragraph("ANNUAL LEAVE CONFIRMATION", styles['Title'])]]
    header_table = Table(header_data, colWidths=[2.5 * inch, 5.5 * inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('VALIGN', (0, 0), (0, 0), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.skyblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, -1), 'Tahoma'),  # Set font to Tahoma
        ('FONTSIZE', (1, 0), (1, 0), 14),
        ('BOTTOMPADDING', (1, 0), (1, 0), 20),  # Increase height of header
        ('TOPPADDING', (1, 0), (1, 0), 10),  # Add top padding
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 18))  # Add space below header

    elements.append(table)

    # Add signatures
    decisions = LeaveDecision.objects.filter(leave=leave)
    signature_rows = []
    current_row = []

    # Add Leave Decisions header
    leave_decision_header_data = [["LEAVE DECISIONS"]]
    leave_decision_header_table = Table(leave_decision_header_data, colWidths=[8 * inch])
    leave_decision_header_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Tahoma'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Increase font size to 12
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.skyblue),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),  # Increase height of header
        ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Add left padding
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Add right padding
        ('TOPPADDING', (0, 0), (-1, -1), 10),  # Add top padding
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Add bottom padding
    ]))
    elements.append(Spacer(1, 20))  # Add space above Leave Decisions header
    elements.append(leave_decision_header_table)

    for decision in decisions:
        if decision.signature and decision.signature.digital_signature:
            try:
                signature_data = decision.signature.digital_signature
                base64_str = signature_data.split(b',')[1]
                decoded_data = base64.b64decode(base64_str)
                signature_io = io.BytesIO(decoded_data)
                pilImage = PILImage.open(signature_io)
                pilImage.verify()
                signature_image = Image(signature_io)
                signature_image.drawHeight = 0.5 * inch  # Reduced size
                signature_image.drawWidth = 1 * inch  # Reduced size
                current_row.append(f"{decision.approvingEmployee.username} ({decision.decisionStatus})")
                current_row.append(signature_image)

                if len(current_row) == 6:  # 3 signatures per row
                    signature_rows.append(current_row)
                    current_row = []
            except (UnidentifiedImageError, IOError) as e:
                error_msg = f"Signature of {decision.approvingEmployee.username} ({decision.decisionStatus}) could not be loaded. Error: {str(e)}"
                print(error_msg)
                current_row.append(error_msg)
                if len(current_row) == 6:
                    signature_rows.append(current_row)
                    current_row = []

    if current_row:  # Add any remaining signatures
        signature_rows.append(current_row)

    # Check if there are signature rows to add to the document
    if signature_rows:
        signature_table = Table(signature_rows,
                                colWidths=[1.5 * inch, 1 * inch, 1.5 * inch, 1 * inch, 1.5 * inch, 1 * inch])
        signature_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Tahoma'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # Increase font size to 12
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Add left padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Add right padding
            ('TOPPADDING', (0, 0), (-1, -1), 10),  # Add top padding
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Add bottom padding
        ]))
        elements.append(signature_table)
    else:
        # Add a placeholder row if no signatures are available
        placeholder_row = [["No decision made yet"]]
        placeholder_table = Table(placeholder_row, colWidths=[6 * inch])
        placeholder_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Tahoma'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),  # Increase font size to 12
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),  # Add left padding
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),  # Add right padding
            ('TOPPADDING', (0, 0), (-1, -1), 10),  # Add top padding
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # Add bottom padding
        ]))
        elements.append(placeholder_table)

    document.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    response = FileResponse(io.BytesIO(pdf), as_attachment=True, filename='leave_info.pdf')
    return response


def add_page_border(canvas, doc):
    canvas.saveState()
    width, height = letter
    margin = 0.5 * inch
    canvas.setLineWidth(2)
    canvas.rect(margin, margin, width - 2 * margin, height - 2 * margin)
    canvas.restoreState()
