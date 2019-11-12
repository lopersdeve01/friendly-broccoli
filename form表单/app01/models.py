from django.db import models

# Create your models here.

class Author(models.Model):
    """
    作者表
    """
    name=models.CharField( max_length=32)
    age=models.IntegerField()
    sex = models.CharField(max_length=16,default='女')
    # authorDetail=models.OneToOneField(to="AuthorDetail",to_field="nid",on_delete=models.CASCADE)
    au=models.OneToOneField("AuthorDetail",on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class AuthorDetail(models.Model):
    """
    作者详细信息表
    """
    birthday=models.DateField()
    telephone=models.CharField(max_length=11)
    addr=models.CharField(max_length=64)
    # class Meta:
        # db_table='authordetail' #指定表名
        # ordering = ['-id',]
    def __str__(self):
        return self.telephone + self.addr


class Publish(models.Model):
    """
    出版社表
    """
    name=models.CharField( max_length=32)
    city=models.CharField( max_length=32)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    书籍表
    """
    title = models.CharField(max_length=32)
    publishDate=models.DateField(null=True)
    price=models.DecimalField(max_digits=5,decimal_places=2)
    publishs=models.ForeignKey(to="Publish",on_delete=models.CASCADE,)
    authors=models.ManyToManyField('Author',)

    def __str__(self):
        return self.title

    def get_authors_name(self):

        return ','.join([i.name for i in self.authors.all()])


class UserInfo(models.Model):
    username=models.CharField(max_length=12)
    bday=models.DateField()
