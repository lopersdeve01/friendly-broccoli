from django.conf.urls import url,include
from web.views import server
urlpatterns = [

    url(r'^index/$', server.index,name='server_index'),           # 首页设置别名，以与其他的index区分
    url(r'^server/add/$', server.server_add,name='server_add'),   # 增加服务器
    url(r'^server/pie/$', server.server_pie,name='server_pie'),   # 增加显示图标，针对ajax实现数据展示
]
