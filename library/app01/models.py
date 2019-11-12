from django.db import models

# Create your models here.

class Publish(models.Model):
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name

class Book(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    # price = models.FloatField()
    price = models.DecimalField(max_digits=5,decimal_places=2)  # 999.99
    publish_date = models.DateField()
    # publish = models.CharField(max_length=32)
    author = models.ManyToManyField(to="Author",)
    publish = models.ForeignKey(to='Publish',to_field="id")  #foreign key(publish) references publish()
    #上面只是简单加上外键，并非进一步的操作
    def __str__(self):
        return self.title


class Author(models.Model):
    name=models.CharField(max_length=32)
    def __str__(self):
        return self.name



