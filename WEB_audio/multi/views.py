from django.shortcuts import render, redirect
from .models import MultiData
from collection.predict import make_wav2img
from multi.apps import MultiConfig


def multiTest(request):
    if request.method == 'POST':
        multi = MultiData.objects.create(
            photo = request.FILES['photo'],
            audio = request.FILES['audio'],
            )
        if not multi.prediction:
            audio_mel_path = make_wav2img(multi.audio.path)
            prediction = predict_multiInput(multi.photo.path, audio_mel_path)
            multi.mel = audio_mel_path[8:]
            multi.prediction = prediction
            multi.save()

        
        return redirect('multiresult')

    else:
        return render(request, 'multi_test.html')