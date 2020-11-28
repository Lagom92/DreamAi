from inferences import predict
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, Xray, Heat, Multi
from inferences.predict import make_wav2img
from inferences.apps import *


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
    if xray.prediction == 'positive':
        heats = Heat.objects.filter(xray=xray)
        return render(request, 'infer.html', {'preds':preds, 'xray':xray, 'heats':heats})

    else:
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
        prediction, nums, cam_list = InferencesConfig.prediction_and_heatmap(xray.photo.path, cxr_model, seg_model, feature_model)
        if prediction == 'positive':
            for cam in cam_list:
                heat = Heat.objects.create(
                    xray = xray,
                    photo = cam[8:]
                )
        xray.prediction = prediction
        xray.save()

        return redirect('inferences:infer', pk, xray.id)

    return render(request, 'examination.html', {'patient':patient})


'''multi inference 검사 페이지'''
def multiExamination(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    if request.method == 'POST':
        multi = Multi.objects.create(
            patient = patient,
            photo = request.FILES['image'],
            audio = request.FILES['audio']
        )
        audio_mel_path = make_wav2img(multi.audio.path)
        prediction = InferencesConfig.predict_multi(multi.photo.path, audio_mel_path)
        multi.mel = audio_mel_path[8:]
        multi.prediction = prediction
        multi.save()

    return render(request, 'multiExamination.html', {'patient':patient})