from django.shortcuts import render, redirect

# Create your views here.


def index_view(request):
    if request.user.is_authenticated:
        return redirect('search_url')
    return redirect('login_url')


def handle_404_view(request, exception=None):
    return render(request, '404.html')
