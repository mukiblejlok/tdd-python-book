from django.shortcuts import render, redirect
from lists.models import Item, List


# Create your views here.
def home_page(request):
    response = render(request,
                      "lists/home.html")
    return response


def view_list(request):
    items = Item.objects.all()
    response = render(request, "lists/list.html", {"items": items})
    return response


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect("/lists/the-only-list-in-the-world/")
