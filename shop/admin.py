from django.contrib import admin
from product.admin import ProductProductTabula
from .models import SaleOrder,User
from import_export import resources
from import_export.admin import ImportExportModelAdmin
import random

class UserResource(resources.ModelResource):
    # @staticmethod
    # def after_import_row(row, row_result, **kwargs):
    #     print("After")
    symbols = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"

    def save_instance(self,instance, using_transactions=True, dry_run=False):
        if not (using_transactions and dry_run):
            super_user = User.objects.get(id=1)
            password = "".join(random.sample(self.symbols,10))
            instance.set_password(password)
            super_user.email_user("Your_password",password,instance.email)
            instance.save()
        else:
            print("I not import")
        
        

    class Meta:
        model = User
        fields = ('id','username', 'first_name','last_name','is_staff','phone', "email" )

class SaleOrderTabula(admin.TabularInline):
	model = SaleOrder
	fk_name = "customer"


# Register your models here.
class UserAdmin(ImportExportModelAdmin):
    '''
        Admin View for Person
    '''
    resource_class = UserResource
    fields = ("username","first_name","last_name","email","phone",)
    list_display = ('__str__','phone','email',)
    inlines = [
        SaleOrderTabula,
    ]


admin.site.register(User, UserAdmin)
class SaleOrderAdmin(admin.ModelAdmin):
    '''
        Admin View for 
    '''
    list_display = ('customer',)
    inlines = [
        ProductProductTabula,
    ]
    

admin.site.register(SaleOrder, SaleOrderAdmin)
