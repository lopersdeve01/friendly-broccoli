from django.shortcuts import render, redirect
from django.http import JsonResponse
from api import models


def index(request):
    server_queryset = models.Server.objects.all()
    return render(request, 'web/index.html', {'queryset': server_queryset})    # server展示页


from django import forms


class ServerModelForm(forms.ModelForm):       # modelForm
    class Meta:
        model = models.Server
        fields = ['hostname', 'status','depart']   # 展示字段

    def __init__(self, *args, **kwargs):           # 封装属性，继承父类（ModelForm）进行属性封装，重新定义子类的参数
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'   # 统一添加类属性
#  这是对继承自父类的属性进行初始化。而且是用父类的初始化方法来初始化继承的属性。

#  也就是说，子类继承了父类的所有属性和方法，父类属性自然会用父类方法来进行初始化。

#  当然，如果初始化的逻辑与父类的不同，不使用父类的方法，自己重新初始化也是可以的。


def server_add(request):
    if request.method == 'GET':        # 查询
        form = ServerModelForm()
        return render(request, 'web/server_add.html', {'form': form})
    form = ServerModelForm(request.POST)    # 添加
    if form.is_valid():
        form.save()
        return redirect('server_index')     
    return render(request, 'web/server_add.html', {'form': form})


def server_pie(request):
    # data_list = [{
    #     "name": '销售部',
    #     "y": 50,
    # }, {
    #     "name": '运维部',
    #     "y": 20
    # }, {
    #     "name": '技术部',
    #     "y": 20
    # }]
    # select coun(depart_id),Depart.title from server 连表 Depart  group by depart_id

    from django.db.models import Count
    result = models.Server.objects.values('depart__title').annotate(ct=Count('depart__title'))  # 准备数据展示需要的数据结构
    data_list = [ {'name':item['depart__title'],'y':item['ct']} for item in result]

    return JsonResponse(data_list,safe=False)
