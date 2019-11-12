from django import forms
# from app01 import models
from rbac import models

# 批量权限使用的form
class MultiPermissionForm(forms.ModelForm):
    class Meta:
        model = models.Permission
        fields = ['title', 'url', 'reverse_name', 'parents', 'menus']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

        self.fields['parents'].choices = [(None, '-------')] + list(
            models.Permission.objects.filter(parents__isnull=True).exclude(
                menus__isnull=True).values_list('id', 'title'))

    def clean(self):
        menu = self.cleaned_data.get('menus')
        pid = self.cleaned_data.get('parents')

        if menu and pid:
            raise forms.ValidationError('菜单和根权限同时只能选择一个')
        return self.cleaned_data