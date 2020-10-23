from django.shortcuts import render

# Create your views here.
def main(request):

    return render(request, 'main.html')


def record(request):

    return render(request, 'record.html')