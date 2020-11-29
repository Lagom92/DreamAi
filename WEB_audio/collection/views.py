from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from collection.apps import CollectionConfig
from .predict import make_wav2img
from .models import Cough, Info

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


'''여러 page version'''

def info(request):
    if request.method == 'POST':
        Info.objects.create(
            age = request.POST['age'],
            region = request.POST['region'],
            sex = request.POST['sex'],
            state = request.POST['state'],

        )

        return redirect('pred')

    return render(request, 'info.html')


@csrf_exempt
def pred(request):
    if request.method == 'POST':
        try:
            Cough.objects.create(
                audio = request.FILES['audio_data'],
                title = str(request.FILES['audio_data'])
            )
        except:
            print("Error in Cough create")

        return redirect('res')
    
    return render(request, 'pred.html')


def res(request):
    cough = Cough.objects.last()
    audio_path = cough.audio.path
    image_path = make_wav2img(audio_path)
    prediction, nums = CollectionConfig.predict_audio(image_path)
    cough.mel = image_path[8:]
    cough.prediction = prediction
    cough.save()

    return render(request, 'res.html', {'prediction':prediction, 'nums':nums})