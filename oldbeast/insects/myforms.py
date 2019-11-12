from insects import models
from django import forms
from multiselectfield.forms.fields import MultiSelectFormField
# 集中处理model表单的表格样式处理

class Customer(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for i_name,i in self.field.items():
            print(type(i))
            if not isinstance(i,MultiSelectFormField):  #多选框。出现select与checkbox中出现multiple的加下面格式会出现前端样式走行，所以排除
                i.widget.attrs.update({'class':'form-control'})



