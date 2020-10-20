from django.http import request
from django.shortcuts import render

# Create your views here.
def main(request):

    return render(request, 'main.html')


def game(request):

    return render(request, 'game.html')