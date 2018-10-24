from django.shortcuts import render
from django.http import HttpResponse

# Testing only
def index(request):
    return render(request, 'index.html', context={
        'test': 'Test'
    })