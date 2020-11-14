import weasyprint
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .shoppinglist import ShoppingList


def shoppinglist_detail(request):
    shoppinglist = ShoppingList(request)
    return render(
        request,
        "purchases/shopList.html",
        {"shoppinglist": shoppinglist, "current_page": "shoppinglist"},
    )


def download_shoppinglist(request):
    shoppinglist = ShoppingList(request)
    ingridients = shoppinglist.get_ingridients_for_pdf()

    html = render_to_string(
        "purchases/pdf.html",
        {"ingridients": ingridients, "shoppinglist": shoppinglist},
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
