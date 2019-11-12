from django.db import models

# Create your models here.
class Author(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    age=models.IntegerField()
    def __str__(self):
        return self.name
authorDetail=models.OneToOneField(to="AuthorDetail",to_field="nid",)
class AuthorDetail(models.Model):
    nid = models.AutoField(primary_key=True)
    birthday=models.DateField()
    telephone=models.BigIntegerField()
    addr=models.CharField( max_length=64)
    def __str__(self):
        return self.addr
class Publish(models.Model):
    nid = models.AutoField(primary_key=True)
    name=models.CharField( max_length=32)
    city=models.CharField( max_length=32)
    def __str__(self):
        return self.name
email=models.EmailField()
class Book(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField( max_length=32)
    publishDate=models.DateField()
    price=models.DecimalField(max_digits=5,decimal_places=2)
    publish=models.ForeignKey(to="Publish",to_field="nid",)
    authors=models.ManyToManyField(to='Author',)
    def __str__(self):
        return self.title