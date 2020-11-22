from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient


'''환자 목록 페이지'''
@login_required
def main(request):
    user = request.user
    patients = Patient.objects.filter(doctor=user).order_by('-id')

    return render(request, 'main.html', {'patients': patients})


'''환자 정보 페이지'''
@login_required
def detail(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    if request.user != patient.doctor:
        return redirect('inferences:main')

    return render(request, 'detail.html', {'patient':patient})


'''환자 정보 수정 페이지'''
@login_required
def editInfo(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    if request.user != patient.doctor:
        return redirect('inferences:main')

    if request.method == 'POST':
        patient.prescription = request.POST['prescription']
        patient.vitalSigns = request.POST['vitalSigns']
        patient.history = request.POST['history']
        patient.save()
        return redirect('inferences:detail', pk)

    return render(request, 'edit_info.html', {'patient':patient})