from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, Xray
from inferences.apps import InferencesConfig


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
    
    xrays = patient.xray.all()

    return render(request, 'detail.html', {'patient':patient, 'xrays':xrays})


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


'''inference 결과 페이지'''
@login_required
def infer(request, pk, img_pk):
    patient = get_object_or_404(Patient, id=pk)
    preds = patient.xray.all().order_by('-created_at')

    xray = get_object_or_404(Xray, id=img_pk)

    return render(request, 'infer.html', {'preds':preds, 'xray':xray})


'''inference 검사 페이지'''
@login_required
def examination(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    if request.method == 'POST':
        xray = Xray.objects.create(
            patient = patient,
            photo = request.FILES['image'],
        )
        xray.prediction = InferencesConfig.predict_CXR(xray.photo.path)
        xray.save()

        return redirect('inferences:infer', pk)

    return render(request, 'examination.html')


