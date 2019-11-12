from django.db import models

# Create your models here.

class Publish(models.Model):
    name = models.CharField(max_length=12)

class Book(models.Model):

    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    # price = models.FloatField()
    price = models.DecimalField(max_digits=5,decimal_places=2)  # 999.99

    publish_date = models.DateField()

    publish = models.CharField(max_length=32)
    # publish_name
    # publish = models.ForeignKey(to='Publish')  #foreign key(publish) references publish()

    def __str__(self):
        return self.title









