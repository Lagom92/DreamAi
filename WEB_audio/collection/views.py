import collection
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Cough
from collection.apps import CollectionConfig
from .predict import make_wav2img

def main(request):

    return render(request, 'main.html')


@csrf_exempt
def audio(request):
    if request.method == 'POST':
        Cough.objects.create(
            audio = request.FILES['audio_data'],
            title = str(request.FILES['audio_data'])
        )
    
    return render(request, 'audio.html')


def infer(request):
    cough = Cough.objects.last()
    audio_path = cough.audio.path
    image_path = make_wav2img(audio_path)
    prediction = CollectionConfig.predict_audio(image_path)
    cough.mel = image_path[8:]
    cough.prediction = prediction
    cough.save()

    return render(request, 'infer.html', {'prediction':prediction})

