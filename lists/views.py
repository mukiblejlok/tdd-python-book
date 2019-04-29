from django.shortcuts import render, redirect
from lists.models import Item


# Create your views here.
def home_page(request):
    if request.method == "POST":
        new_item = Item()
        post_text = request.POST.get('item_text', '')
        new_item.text = post_text
        new_item.save()
        return redirect("/")


    response = render(request,
                      "lists/home.html", {"items": Item.objects.all()})
    return response
