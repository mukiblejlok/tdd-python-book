from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    data = {'new_item_text': request.POST.get('item_text', '')}

    response = render(request,
                      "lists/home.html",
                      data)
    return response
