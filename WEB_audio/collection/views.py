from django.shortcuts import render


def main(request):

    return render(request, 'main.html')


def audio(request):

    return render(request, 'audio.html')


def aud(request):

    return render(request, 'aud.html')
