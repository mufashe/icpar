from django.shortcuts import redirect, render, get_object_or_404

from company.forms.userAsEmployeeSignatureForm import UserAsEmployeeSignatureForm
from company.models import EmployeeAsUserSignature


def createSignature(request):
    signatureForm = UserAsEmployeeSignatureForm()
    if request.method == 'POST':
        signatureForm = UserAsEmployeeSignatureForm(request.POST, request.FILES)
        if signatureForm.is_valid():
            employee_id = signatureForm.cleaned_data.get('employee').id
            existingSignature = EmployeeAsUserSignature.objects.filter(employee_id=employee_id).first()
            if existingSignature:
                existingSignature.digital_signature = request.POST.get('digital_signature').encode('utf-8')
                existingSignature.signature_password = signatureForm.cleaned_data.get('signature_password')
                existingSignature.save()
                return redirect('cresig')
            else:
                signature_instance = signatureForm.save(commit=False)
                signature_data = request.POST.get('digital_signature')
                signature_instance.digital_signature = signature_data.encode('utf-8')
                signature_instance.save()
                return redirect('cresig')
    else:
        signatureForm = UserAsEmployeeSignatureForm()

    context = {'signatureForm': signatureForm}
    return render(request, 'company/employee/signature.html', context)


def displayEmployeeSignature(request, pk):
    signature_instance = get_object_or_404(EmployeeAsUserSignature, employee__id=pk)
    signatureImage = signature_instance.digital_signature.decode(
        'utf-8') if signature_instance.digital_signature else None
    context = {'signature': signatureImage}

    return render(request, 'company/employee/employeeSignature.html', context)
