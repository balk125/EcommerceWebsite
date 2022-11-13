from distutils.command.upload import upload
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models


# Create your models here.
class product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category =models.CharField(max_length=50,default="")
    subcategory =models.CharField(max_length=50,default="")
    price=models.IntegerField(default=0)
    
    desc=models.CharField(max_length=3000 )
    product_time=models.DateTimeField()
    image=models.ImageField(upload_to="shop/images",default="")


    def __str__(self) :
        return self.product_name




class Contact(models.Model):
    msg_Id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=100,default='')
    phone=models.CharField(max_length=70,default='')
    desc=models.CharField(max_length=500,default='')

    def __str__(self) :
        return self.name

 
class orders(models.Model):
    order_id=models.AutoField(primary_key=True )
    # order_id2=models.IntegerField(default=-1)
    
    items_json=models.CharField(max_length=5000)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=108,default='')
    email=models.CharField(max_length=108,default='') 
    address=models.CharField(max_length=108,default='')
    city=models.CharField(max_length=108,default='')
    state=models.CharField(max_length=108,default='')
    zip_code=models.CharField(max_length=108,default='')
    phone=models.CharField(max_length=70,default='')
    


    def __str__(self) :
        return self.name


class orderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True )
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)
    
    def __str__(self) :
        # return self.update_desc[0:14]+ "..."
        return f'order id : {self.order_id}'
