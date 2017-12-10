from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import User, SaleOrder
from product.models import Category, ProductTemplate, ProductProduct
from datetime import date
from django.db.models import Sum
# Create your views here.


class My_shop_view:
    """docstring for My_view"""

    @staticmethod
    def list_customer(request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/login/?next=/list_customer/")
        users = User.objects.all()
        customers = []
        today = date.today()
        for user in users:
            customer = {"name": user}
            sale_order = user.sale_order.all()[len(
                user.sale_order.all())-1] if len(user.sale_order.all()) >= 1 else False
            if sale_order:
                if (sale_order.date_reserve == today or
                        sale_order.date_order_confirm == today or
                        sale_order.confirmed):

                    customer.update({
                        "products": sale_order.list_product.all(),
                        "confirmed": sale_order.confirmed,
                        "total": sale_order.total()})
                else:
                    customer.update({"products": False, "confirmed": False})
            else:
                customer.update({"products": False, "confirmed": False})

            customers.append(customer)
        context = {
            'My_title': 'List Users',
            'customers': customers
        }
        return render(request, "shop/templates/customer_list.html", context)

    @staticmethod
    def delete_sale_order(request):
        id_row = request.GET.get("id_row")
        SaleOrder.objects.get(id=id_row).delete()
        return HttpResponseRedirect("/list_customer/")

    @staticmethod
    def confirmed(request):
        id_row = request.GET.get("id_row")
        sale_order = SaleOrder.objects.get(id=id_row)
        sale_order.sale_confirm(request.user)
        return HttpResponseRedirect("/list_customer/")

    @staticmethod
    def update_sale_order(request, slug):
        sale_order = SaleOrder.objects.get(slug=slug)
        if request.method == "POST":
            product_temp = request.POST.getlist("product_template")
            if product_temp:
                for id_temp in product_temp:
                    temp = ProductTemplate.objects.get(id=int(id_temp))
                    list_product = sale_order.list_product
                    product_product = list_product.filter(
                        product_template=temp)
                    if len(product_product) > 0:
                        product_product[0].count_product += 1

                        product_product[0].save()
                    else:
                        sale_order.list_product.create(
                            product_template=temp, count_product=1)
            # sale_order.list_product.create()

        context = {
            "title": "Edit",
            "sale_order": sale_order
        }
        return render(request, "shop/templates/edit_sale_order.html", context)
