from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Cough


def main(request):

    return render(request, 'main.html')


@csrf_exempt
def audio(request):
    if request.method == 'POST':
        Cough.objects.create(
            audio = request.FILES['audio_data'],
            name = str(request.FILES['audio_data'])
        )
    
    return render(request, 'audio.html')


def infer(request):
    cough = Cough.objects.last()

    infer = "cough test infer"

    return render(request, 'infer.html', {'infer':infer})

