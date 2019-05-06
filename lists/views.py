from django.shortcuts import render, redirect
from lists.models import Item


# Create your views here.
def home_page(request):
    if request.method == "POST":
        # new_item = Item()
        # post_text = request.POST.get('item_text', '')
        # new_item.text = post_text
        # new_item.save()
        # # above is can be shortened to
        Item.objects.create(text=request.POST.get('item_text', ''))

        return redirect("/lists/the-only-list-in-the-world/")

    # items = Item.objects.all()
    response = render(request,
                      "lists/home.html")
    return response


def view_list(request):
    items = Item.objects.all()
    response = render(request, "lists/list.html", {"items": items})
    return response
