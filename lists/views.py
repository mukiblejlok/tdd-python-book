from django.shortcuts import render


# Create your views here.
def home_page(request):
    respose = render(request, "lists/home.html")
    return respose
