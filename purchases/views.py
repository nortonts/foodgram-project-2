import weasyprint
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .shoppinglist import ShoppingList


def shoppinglist_detail(request):
    shopping_list = ShoppingList(request)
    return render(
        request,
        "purchases/shopList.html",
        {"shopping_list": shopping_list, "current_page": "shopping_list"},
    )


def download_shoppinglist(request):
    shopping_list = ShoppingList(request)
    ingridients = shopping_list.get_ingridients_for_pdf()

    html = render_to_string(
        "purchases/pdf.html",
        {"ingridients": ingridients, "shopping_list": shopping_list},
    )
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'filename="shoppinglist.pdf"'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(settings.BASE_DIR + "/purchases/static/css/pdf.css")
        ],
    )
    return response
