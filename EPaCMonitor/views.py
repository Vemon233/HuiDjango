from django.shortcuts import render


# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)


def about(request):
    context_dict = {}
    return render(request, 'about.html', context_dict)


def pathogen(request):
    context_dict = {}
    return render(request, 'pathogen.html', context_dict)


def board(request):
    context_dict = {}
    return render(request, 'board.html', context_dict)


def undiagnosed(request):
    context_dict = {}
    return render(request, 'undiagnosed.html', context_dict)
