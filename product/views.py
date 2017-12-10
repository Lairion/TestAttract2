from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import Category, ProductProduct
from datetime import date
from shop.models import SaleOrder
import json
# Create your views here.


class My_product_view:
    """docstring for My_view"""
    @staticmethod
    def list_product(request):
        if not request.user.is_authenticated:
            return redirect("/login/")
        today = date.today()
        req_so_id = request.GET.get("so_id", None)
        if req_so_id:
            sale_order = SaleOrder.objects.get(id=req_so_id)
        else:
            sale_order = SaleOrder.objects.create(
                date_reserve=today, customer=request.user)
            sale_order.save()
        categories = Category.objects.all()
        context = {
            "title": "Products",
            "categories": categories,
            "slug": sale_order.slug
        }
        return render(request, "product/templates/product_list.html", context)

    @staticmethod
    def delete_product(request):
        get_id = request.POST.get("id_product")
        so_id = request.POST.get("sale_order")
        product = ProductProduct.objects.filter(id=int(get_id))
        product[0].delete()

        return HttpResponse(json.dumps({
            'redirect': "/sale_order/sale-number-"+so_id+"/"}),
            content_type="application/json")

    @staticmethod
    def update_product(request):
        get_id = request.POST.get("id_product")
        so_id = request.POST.get("sale_order")
        count_product = request.POST.get("count_product")
        product = ProductProduct.objects.get(id=int(get_id))
        product.count_product = int(count_product)
        product.save()
        return HttpResponse(json.dumps({
            'redirect': "/sale_order/sale-number-"+so_id+"/"}),
            content_type="application/json")

        return HttpResponseRedirect("/create_sale_order/")
