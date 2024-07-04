from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
# from django.utils.safestring import mark_safe


from userauths.models import User

STATUS_CHOICE = {
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
}

STATUS = {
    ("draft", "Processing"),
    ("disabled", "Shipped"),
    ("rejected", "Delivered"),
    ("in_review", "In Review"),
    ("rejected", "Rejected"),
}

RATING = {
    ( 1,  "★☆☆☆☆"),
    ( 2,  "★★☆☆☆"),
    ( 3,  "★★★☆☆"),
    ( 4,  "★★★★☆"),
    ( 5,  "★★★★★"),
}

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    """Model definition for Category."""
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat', alphabet='abcdefghijklmnopqrstuvwxyz9871234')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', default='category.jpg')
    
    # TODO: Define fields here

    class Meta:
        """Meta definition for Category."""

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50">'% (self.image.url))

    def __str__(self):
        """Unicode representation of Category."""
        return self.title
    
class Tags(models.Model):
    """Model definition for Tags."""

    # TODO: Define fields here

    class Meta:
        """Meta definition for Tags."""

        verbose_name = 'Tags'
        verbose_name_plural = 'Tags'

    def __str__(self):
        """Unicode representation of Tags."""
        pass

    
class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven', alphabet='abcdefghijklmnopqrstuvwxyz9871234')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100, default='132 Sure wound care clinic.')
    contact = models.CharField(max_length=100, default='+233 24 387 6338')
    chat_resp_time = models.CharField(max_length=100, default='100')
    shipping_on_time = models.CharField(max_length=100, default='100')
    authentic_rating = models.CharField(max_length=100, default='100')
    days_return = models.CharField(max_length=100, default='100')
    warranty_period = models.CharField(max_length=100, default='100')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        """Meta definition for Vendor."""

        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'

    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50">'% (self.image.url))

    def __str__(self):
        """Unicode representation of Vendor."""
        return self.title
    

class Product(models.Model):
    """Model definition for Product."""
    pid = ShortUUIDField(unique=True, length=10, max_length=20, alphabet='abcdefghijklmnopqrstuvwxyz9871234')
    title = models.CharField(max_length=100, default='Bass Speaker Setereo 2.0')
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = models.TextField(null=True, blank=True, default='I am an amazing vendor.')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default='1.99')
    old_price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default='2.99')
    specifications = models.TextField(null=True, blank=True, default='This is the product.')
    tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(max_length=100, choices=STATUS, default='in_review')
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix='sku', alphabet='1234567890')
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50">'% (self.image.url))


    def __str__(self):
        """Unicode representation of Product."""
        return self.title
    
    def get_percentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
class ProductImages(models.Model):
    """Model definition for ProductImages."""

    images = models.ImageField(upload_to='product_images', default='product.jpg')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for ProductImages."""

        verbose_name = 'Product Images'
        verbose_name_plural = 'Product Images'


############################################## Cart, Order, OrderItems #################################################
############################################## Cart, Order, OrderItems #################################################
############################################## Cart, Order, OrderItems #################################################
############################################## Cart, Order, OrderItems #################################################

class CartOrder(models.Model):
    """Model definition for CartOrder."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default='1.99')
    paid_status = models.BooleanField(default=True)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(max_length=30, choices=STATUS_CHOICE, default='processing')

    class Meta:
        """Meta definition for CartOrder."""

        verbose_name = 'Cart Order'
        verbose_name_plural = 'Cart Order'

class CartOrderItems(models.Model):
    """Model definition for CartOrderItems."""
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE, null=True)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.ImageField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999999999999, decimal_places=2, default='1.99')
    total = models.DecimalField(max_digits=99999999999999, decimal_places=2, default='1.99')

    class Meta:
        """Meta definition for CartOrderItems."""

        verbose_name = 'Cart Order Items'
        verbose_name_plural = 'Cart Order Items'

    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50">'% (self.image))


############################################## Product, Review, Wishlists and Address #################################################
############################################## Product, Review, Wishlists and Address #################################################
############################################## Product, Review, Wishlists and Address #################################################
############################################## Product, Review, Wishlists and Address #################################################



class ProductReview(models.Model):
    """Model definition for ProductReview."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=STATUS, default=None)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for ProductReview."""

        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'

    def __str__(self):
        """Unicode representation of ProductReview."""
        self.product.title

    def get_rating(self):
        return self.rating
    
class WishLists(models.Model):
    """Model definition for Wishlists."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Wishlists."""

        verbose_name = 'Wishlists'
        verbose_name_plural = 'Wishlists'

    def __str__(self):
        """Unicode representation of Wishlists."""
        self.product.title

class Address(models.Model):
    """Model definition for Address."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        """Meta definition for Address."""

        verbose_name = 'Address'
        verbose_name_plural = 'Address'

    def __str__(self):
        """Unicode representation of Address."""
        self.product.title

