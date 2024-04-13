from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Category(models.Model):
    category=models.CharField(max_length=255)
class Book(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    book_name=models.CharField(max_length=255)
    book_description=models.CharField(max_length=255)
    auther_name=models.CharField(max_length=255)
    book_stock=models.IntegerField()
    book_price=models.IntegerField()
    Image=models.ImageField(upload_to="image/",null=True)
    isbn=models.PositiveBigIntegerField()
    book_rent=models.IntegerField()
class Usermember(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    number=models.CharField(max_length=12)
    uImage=models.ImageField(upload_to="image/", null=True)
    status=models.IntegerField(default=0)
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    quantity= models.IntegerField(default=0)    
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    
User.cart = property(lambda u: Cart.objects.get_or_create(user=u)[0])
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    Email=models.EmailField()
    Address=models.CharField(max_length=255)
    phone=models.CharField(max_length=12)
    city=models.CharField(max_length=255)
    State=models.CharField(max_length=255)
    country=models.CharField(max_length=255)
    pincode=models.CharField(max_length=255)
    total_price=models.CharField(max_length=255)
    payment_mode=models.CharField(max_length=255)
    payment_id=models.CharField(max_length=255)
    tracking_no=models.CharField(max_length=255,null=True)
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,null=True)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    price=models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Contact(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=225)
    email=models.EmailField()
    Message=models.CharField(max_length=225)




class Rent(models.Model):
    Issuedate=models.DateField(blank=True,null=True)
    returndate=models.DateField(blank=True,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    status=models.IntegerField(default=0)

class Requestbook(models.Model):
    Issuedate=models.DateField(blank=True,null=True)
    returndate=models.DateField(blank=True,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    issued=models.BooleanField(default=False)
    returned=models.BooleanField(default=False)
    amount=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    paid=models.BooleanField(default=False)
    diff=models.PositiveIntegerField(default=0)
    status=models.IntegerField(default=0)
    calc=models.BooleanField(default=False)


    def days_no(self):
        "Returns the no. of days before returning / after return_date."
        if self.issued:
            y,m,d=str(timezone.now().date()).split('-')
            today=datetime.date(int(y),int(m),int(d))
            y2,m2,d2=str(self.returndate).split('-')
            lastdate=datetime.date(int(y2),int(m2),int(d2))
            if lastdate > today:
                return "{} left".format(str(lastdate-today).split(',')[0])
            else:
                return "{} passed".format(str(today-lastdate).split(',')[0])
        else:
            return ""









class Issuebook(models.Model):
    Issuedate=models.DateField(blank=True,null=True)
    returndate=models.DateField(blank=True,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    issued=models.BooleanField(default=False)
    returned=models.BooleanField(default=False)
    amount=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    paid=models.BooleanField(default=False)
    diff=models.PositiveIntegerField(default=0)
    status=models.PositiveIntegerField(default=0)



class Issue(models.Model):
    Issuedate=models.DateField(blank=True,null=True)
    returndate=models.DateField(blank=True,null=True)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    rent=models.ForeignKey(Rent,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=0)
    issued=models.BooleanField(default=False)
    returned=models.BooleanField(default=False)
    amount=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    status=models.IntegerField(default=0)

class Lost(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField(default=0)
    status=models.IntegerField(default=0)
    damage=models.CharField(max_length=255)
    fine=models.PositiveIntegerField(default=0.00)
    subtotal=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    penalty=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    bookfine=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)




    
class Pay(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    fineamout=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField(default=0)

class Paydetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    Email=models.EmailField()
    fname=models.CharField(max_length=255)
    lname=models.CharField(max_length=255)
    phone=models.CharField(max_length=12)
    total_price=models.CharField(max_length=255)
class Payment(models.Model):
    paydetails=models.ForeignKey(Paydetails, on_delete=models.CASCADE)
    fineamout=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    book=models.ForeignKey(Book,on_delete=models.CASCADE,null=True)
    quantity=models.PositiveIntegerField(default=0)
class Bookfine(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    requestbook=models.ForeignKey(Requestbook,on_delete=models.CASCADE)
    amount=models.DecimalField(default=0.00,max_digits=10,decimal_places=2)
    paid=models.BooleanField(default=False)
    diff=models.PositiveIntegerField(default=0)
    status=models.IntegerField(default=0)












