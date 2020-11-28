from django.shortcuts import render, redirect
from .models import MultiData
from multi.predict import make_wav2img, predict_multiInput
from multi.apps import MultiConfig


def multiTest(request):
    if request.method == 'POST':
        multi = MultiData.objects.create(
            photo = request.FILES['photo'],
            audio = request.FILES['audio'],
            )
        if not multi.prediction:
            audio_mel_path = make_wav2img(multi.audio.path)
            prediction, nums = predict_multiInput(multi.photo.path, audio_mel_path)
            multi.neg_rate, multi.pos_rate = nums
            multi.mel = audio_mel_path[8:]
            multi.prediction = prediction
            multi.save()

        return redirect('multiResult')

    else:
        return render(request, 'multi_test.html')


def multiResult(request):
    multi = MultiData.objects.last()

    return render(request, 'multiResult.html', {'multi':multi})