from django.db import models
# Create your models here.
from django.utils.text import slugify
class Category(models.Model):
    """
    Description: Model Description
    """
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100,null=True,blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        categories = Category.objects.filter(name=self.name).exclude(id=self.id)
        if len(categories) > 0:
            self.slug += "-" + str(self.id) 
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        pass
class ProductTemplate(models.Model):
    """
    Description: Model Description
    """
    image = models.ImageField(upload_to="food_image")
    name = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name="product_template")
    price = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    slug = models.SlugField(max_length=100,null=True,blank=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        productsT = ProductTemplate.objects.filter(name=self.name).exclude(id=self.id)
        if len(productsT) > 0:
            self.slug += "-" + str(self.id) 
        super(ProductTemplate, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse("product:template",kwargs = {"slug":self.slug})

    class Meta:
        pass
class ProductProduct(models.Model):
    """
    Description: Model Description
 list_product/   """
    sale_order = models.ForeignKey('shop.SaleOrder', related_name="list_product")
    product_template = models.ForeignKey(ProductTemplate,related_name="product_product")
    count_product = models.IntegerField(default=1)
    amount_total = models.DecimalField( max_digits=5, decimal_places=2, null=True,blank=True)
    def __str__(self):
        return "%s %s X %s" % (self.product_template.name, self.product_template.price, self.count_product)

    def save(self, *args, **kwargs):
        self.amount_total = self.product_template.price * int(self.count_product)
        super(ProductProduct, self).save(*args, **kwargs)

    

    class Meta:
        pass