from django.shortcuts import render


# The welcome page of the platform
def welcome(request):
    return render(request, 'index.html')


# A help page with the theme examples to speed up development
def help(request):
    return render(request, 'help/index.html')
