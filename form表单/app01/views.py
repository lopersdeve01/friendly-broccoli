from django.shortcuts import render,HttpResponse,redirect
from django import forms
from app01 import models
# Create your views here.

def home(request):
    if request.method=='GET':
        obj = models.Book.objects.all()
        author=models.Author.objects.all()
        publish=models.Publish.objects.all()

        return render(request, 'home.html', {'obj': obj,'author':author,'publish':publish})

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')

class UserInfo(forms.Form):
    username=forms.CharField(
        label='username',
        # widget=forms.widgets.TextInput(),
        initial='the old beast',
        # min_length=6,
        max_length=12,
        # required=True,
        error_messages={
            'required':'不能为空',
            'min_length':'太短了',
            'max_length':'太长了',
        },
        # validators=[mobile_validate,RegexValidator(r'^a','必须以‘a’开头！'),RegexValidator('b$','必须以‘b’结尾！')],
    )

    password=forms.CharField(
        label='password',
        initial='insects',
        widget=forms.widgets.PasswordInput(attrs={'class':'c1'},render_value=True),
    )
    r_password=forms.CharField(
        label='r_password',
        widget=forms.widgets.PasswordInput(attrs={'class': 'c1'},render_value=True),
    )

    sex = forms.ChoiceField(
        choices=((1,'女'),(2,'男'),),
        widget=forms.RadioSelect,
        # widget=forms.widgets.Select,
    )
    hobby = forms.MultipleChoiceField(
        choices= ((1,'喝酒'),(2,'抽烟'),(3,'烫头')),
        # widget=forms.SelectMultiple,
        widget=forms.CheckboxSelectMultiple,
    )

    remember_me = forms.ChoiceField(
        label='记住我',

        widget=forms.CheckboxInput,
    )

    bday = forms.DateField(
        label='出生日期',
        widget=forms.DateInput(attrs={'type':'date'}),  # 日期类型必须加上日期属性

    )
    def clean_username(self):
        value=self.cleaned_data.get('username')
        if '666' in value:
            raise  ValidationError('光喊666是不行的')
        else:
            return value
    def clean(self):
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')
        if password == r_password:
            return self.cleaned_data
        else:
            # raise ValidationError('两次密码不一致！！！！')
            self.add_error('r_password', '两次密码不一致~~~~')  # 给单独的某个字段加错误信息


def login(request):
    obj=UserInfo()

    if request.method=='GET':
        return render(request,'login.html',{'obj':obj})
    else:
        obj1=UserInfo(request.POST)
        if obj1.is_valid():
            print('正确数据',obj1.cleaned_data)
        else:
            print('错误信息',obj1.errors)
        return render(request,'login.html',{'obj':obj1})










class AddBookForm(forms.Form):
    title=forms.CharField(
        label='title',
    )
    price=forms.DecimalField(
        label='price',
        max_digits=5,
        decimal_places=3,
    )
    publishDate=forms.CharField(
        label='publishDate',
        widget=forms.TextInput(attrs={'type':'date'}),
    )
    # publishs_id = forms.ChoiceField(
    #     choices=models.Publish.objects.all().values_list('id','name'),  #[(),()]
    # )
    # authors=forms.MultipleChoiceField(
    #     choices=models.Author.objects.all().values_list('id','name')
    #
    # )

    publishs = forms.ModelChoiceField(
        queryset=models.Publish.objects.all(),
    )
    authors = forms.ModelMultipleChoiceField(
        queryset=models.Author.objects.all(),

    )

    csrfmiddlewaretoken = forms.ChoiceField
    # 批量添加属性样式
    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field_name,field in self.fields.items(): #orderdict(('username',charfield对象))

            field.widget.attrs.update({'class':'form-control'})

# def addbook(request):
#     if request.method=='GET':
#         book=AddBookForm()
#         return render(request,'addbook.html',{'book':book})
#     else:
#         book=AddBookForm(request.POST)
#         if book.is_valid():
#             print(book.cleaned_data)
#             return HttpResponse('OK')
#         else:
#             return render(request,'addbook.html',{'book':book})


class BookModelForm(forms.ModelForm):
    class Meta:
        model=models.Book
        fields='__all__'
        labels={'title':"title",'price':'Price','publishDates':'publishDates'}
        widgets={'publishDates':forms.DateInput(attrs={'type':'date'}),'title':forms.TextInput(attrs={'type':'text'}),}
        error_messages={'title':{'required':'not null'},'price':{'required':'not null'},}



def addbook(request):
    if request.method=='GET':
        book_model=BookModelForm()
        return render(request,'addbook.html',{'book':book_model})
    else:
        book_model = BookModelForm(request.POST)
        print(request.POST)  # {'title':'xx'}
        if book_model.is_valid():
            print(book_model.cleaned_data)
            book_model.save()
            return redirect('showbooks')
        else:
            return render(request, 'addbook.html', {'book': book_model})


def editbook(request,book_id):
    old_objs = models.Book.objects.filter(pk=book_id) #

    if request.method == 'GET':
        # all_publish = models.Publish.objects.all()
        # all_authors = models.Author.objects.all()
        old_obj = old_objs.first()
        book_model_obj = BookModelForm(instance=old_obj)


        return render(request,'editbook.html',{'book_model_obj':book_model_obj})
        # return render(request,'editbook.html',{'all_publish':all_publish,'all_authors':all_authors,'old_obj':old_obj})
    else:

        book_model_obj = BookModelForm(request.POST,instance=old_objs.first())
        if book_model_obj.is_valid():
            book_model_obj.save()# 不写instance就是create值操作  #有就是 update
            return redirect('showbooks')
        else:
            return render(request,'editbook.html',{'book_model_obj':book_model_obj})
        # authors = request.POST.getlist('authors')
        # print('authors',authors)
        # data = request.POST.dict()
        # data.pop('csrfmiddlewaretoken')
        # data.pop('authors')
        #
        # print(data)
        #
        # old_objs.update(**data)
        # old_objs.first().authors.set(authors)

        # return redirect('showbooks')


