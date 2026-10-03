from django.db import models

class Valuation(models.Model):
    product_sku = models.TextField()
    cs = models.IntegerField()
    ib =  models.IntegerField()
    pcs =  models.IntegerField()
    def __str__(self):
        return self.product_sku

class Count(models.Model):
    product_sku = models.TextField()
    cs = models.IntegerField()
    ib =  models.IntegerField()
    pcs =  models.IntegerField()
    def __str__(self):
        return self.product_sku

class Badstock(models.Model):
    product_sku = models.TextField()
    cs = models.IntegerField()
    ib =  models.IntegerField()
    pcs =  models.IntegerField()
    remarks = models.TextField(default='-')
    def __str__(self):
        return self.product_sku

class Undelivered(models.Model):
    product_sku = models.TextField()
    cs = models.IntegerField()
    ib =  models.IntegerField()
    pcs =  models.IntegerField()
    def __str__(self):
        return self.product_sku

class Product(models.Model):
    product_sku = models.TextField(default="-")
    description = models.TextField(default="-")
    qtyperpcs = models.IntegerField(default=0)
    bccs =  models.TextField(default="-")
    bcib =  models.TextField(default="-")
    bcpcs =  models.TextField(default="-")

    def cs_ib_pcs(self):
        val = Valuation.objects.filter(product_sku=self.product_sku).first()
        if val:
            return (f"{val.cs}-{val.ib}-{val.pcs}")
        else:
            return 0

    def badstock(self):
        bs = Badstock.objects.filter(product_sku=self.product_sku).first()
        if bs:
            return (f"{bs.cs}-{bs.ib}-{bs.pcs}")
        else:
            return 0

    def undelivered(self):
        ud = Undelivered.objects.filter(product_sku=self.product_sku).first()
        if ud:
            return (f"{ud.cs}-{ud.ib}-{ud.pcs}")
        else:
            return 0

    def __str__(self):
        return self.product_sku

class Promo(models.Model):
    promo_sku = models.TextField(default="-")
    product_sku = models.TextField(default="-")
    mech_per_pcs = models.IntegerField(default=1)

    def get_description(self):
        associated_product = Product.objects.filter(product_sku=self.promo_sku).first()
        return associated_product.description if associated_product else "DEFAULT"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        product = Product.objects.filter(product_sku=self.product_sku).first()
        if product:
            PromoProduct.objects.create(promo=self, product=product)
        else:
            product = Product.objects.filter(product_sku='DEFAULT').first()
            PromoProduct.objects.create(promo=self, product=product)

    def __str__(self):
        return self.promo_sku

class PromoProduct(models.Model):
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return f"{self.promo} - {self.product}"

