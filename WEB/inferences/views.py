from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    user = request.user
    print("main-----------")
    print(user)

    return render(request, 'main.html')