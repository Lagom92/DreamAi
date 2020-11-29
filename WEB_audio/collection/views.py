from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from collection.apps import CollectionConfig
from .predict import make_wav2img
from .models import Cough

def index(request):

    return render(request, 'index.html')


@csrf_exempt
def audio(request):
    if request.method == 'POST':
        try:
            Cough.objects.create(
                audio = request.FILES['audio_data'],
                title = str(request.FILES['audio_data'])
            )
        except:
            print("Error in Cough create")
    
    return render(request, 'index.html')


def infer(request):
    cough = Cough.objects.last()
    audio_path = cough.audio.path
    image_path = make_wav2img(audio_path)
    pred, nums = CollectionConfig.predict_audio(image_path)
    cough.mel = image_path[8:]
    cough.prediction = pred
    cough.save()

    return render(request, 'infer.html', {'prediction':pred, 'nums':nums})
