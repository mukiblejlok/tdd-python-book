from django.shortcuts import render, redirect
from lists.models import Item, List


# Create your views here.
def home_page(request):
    response = render(request,
                      "lists/home.html")
    return response


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)
    response = render(request, "lists/list.html", {"list": list_})
    return response


def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'],
                        list=list_)
    return redirect(f"/lists/{list_.id}/")


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f"/lists/{list_.id}/")
