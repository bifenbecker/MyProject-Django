from django.shortcuts import render
from .models import Item

# Create your views here.


def search_view(request):
    return render(request, "search.html", context={'items': Item.objects.all()})
