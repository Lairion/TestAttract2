from django.contrib import admin
from .models import Category,ProductTemplate,ProductProduct
# Register your models here.
class ProductProductTabula(admin.TabularInline):
	model = ProductProduct
class ProductTemplateTabula(admin.TabularInline):
	model = ProductTemplate
	fields = ('image','name','description',"price",)

class CategoryAdmin(admin.ModelAdmin):
    '''
        Admin View for 
    '''
    fields = ('name',)
    list_display = ('name',)
    inlines = [
        ProductTemplateTabula,
    ]

class ProductTemplateAdmin(admin.ModelAdmin):
    '''
        Admin View for 
    '''
    list_display = ('name','category',)
    fields = ('image','name','description',"price",)
    inlines = [
        ProductProductTabula,
    ]

admin.site.register(Category,CategoryAdmin)
admin.site.register(ProductTemplate, ProductTemplateAdmin)
admin.site.register(ProductProduct)