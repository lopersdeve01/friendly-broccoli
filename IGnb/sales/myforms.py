from sales import models
from django import forms



class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=4,
        error_messages={
            'max_length':'太长了',
            'min_length':'太短了,你不行',
            'required':'不能为空',
        },
        widget=forms.TextInput(attrs={'class':'username','placeholder':'您的用户名','autocomplete':'off'})
    )

    password = forms.CharField(
        max_length=32,
        error_messages={
            'required': '不能为空',
            'max_length': '不能太长',
        },
        widget=forms.PasswordInput(attrs={'class':'password','placeholder':'输入密码'
            ,'oncontextmenu':'return false','onpaste':'return false'}),

    )

    confirm_password = forms.CharField(
        max_length=32,
        error_messages={
            'required': '不能为空',
            'max_length': '不能太长',
        },
        widget=forms.PasswordInput(attrs={'class': 'confirm_password', 'placeholder': '输入密码'
            , 'oncontextmenu': 'return false', 'onpaste': 'return false'}),
    )

    telephone = forms.CharField(
        max_length=11,
        min_length=11,
        error_messages={
            'max_length': '不能太长,需11位',
            'min_length': '不能太短,需11位',
            'required':'不能为空'
        },
        widget=forms.TextInput(attrs={'class':'phone_number','placeholder':'输入手机号码','autocomplete':'off','id':'number'})

    )

    email = forms.EmailField(
        error_messages={
            'invalid': '必须是邮箱格式',
            'required': '不能为空'
        },
        widget=forms.EmailInput(
            attrs={ 'class': 'email', 'placeholder': '输入邮箱地址',
                   'oncontextmenu': 'return false','onpaste': 'return false'})

    )

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return self.cleaned_data

        else:
            self.add_error('confirm_password','两次密码不一致!')



class CustomerModelForm(forms.ModelForm):

    class Meta:
        model = models.Customer
        fields = '__all__'


    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field_name,field in self.fields.items():
            print(type(field))
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):

                field.widget.attrs.update({'class':'form-control'})


class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status',]

    def __init__(self,request,*args,**kwargs):

        super().__init__(*args,**kwargs)

        for field_name,field in self.fields.items():
            if field_name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant__username=request.session.get('username'))
            if field_name == 'consultant':
                # obj = models.UserInfo.objects.filter(username=request.session.get('username')).first()
                # field.choices = ((obj.pk,obj.username),)
                field.queryset = models.UserInfo.objects.filter(username=request.session.get('username'))

            field.widget.attrs.update({'class':'form-control'})




