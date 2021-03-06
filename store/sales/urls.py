from django.conf.urls import url
from django.contrib import admin
from sales.views import auth,customer

urlpatterns = [

    # 登录
    url(r'^login/', auth.login,name='login'),
    # 注销
    url(r'^logout/', auth.logout,name='logout'),
    # 注册
    url(r'^register/', auth.register,name='register'),


    # 首页
    url(r'^home/', customer.home,name='home'),
    # 公户信息展示
    # url(r'^customers/', views.customers,name='customers'),
    url(r'^customers/', customer.Customers.as_view(),name='customers'),
    # 私户信息展示
    url(r'^mycustomers/', customer.Customers.as_view(),name='mycustomers'),
    # 添加客户
    url(r'^addcustomer/', customer.addEditCustomer,name='addcustomer'),
    # 编辑客户
    url(r'^editcustomer/(\d+)/', customer.addEditCustomer,name='editcustomer'),

    # 跟进记录展示
    url(r'^consultrecords/', customer.ConsultRecord.as_view(),name='consultrecords'),
    # 跟进记录增加和编辑
    url(r'^addConsultRecord/', customer.addEditConsultRecord,name='addConsultRecord'),
    url(r'^editConsultRecord/(\d+)/', customer.addEditConsultRecord,name='editConsultRecord'),


    #报名记录展示
    url(r'^enrollmentrecords/', customer.enrollmentrecord, name='enrollmentrecords'),
    # 跟进记录增加和编辑
    url(r'^addEnrollmentRecords/', customer.addEditEnrollmentRecord, name='addenrrollmentrecords'),
    url(r'^editEnrollmentRecords/(\d+)/', customer.addEditEnrollmentRecord, name='editenrollmentrecords'),
    url(r'^deleteEnrollmentRecords/(\d+)/', customer.deleteEnrollmentRecord, name='deleteenrollmentrecords'),
    url(r'^bulkdelete/', customer.bulkdelete, name='bulkdelete'),

    # # 学习记录展示
    # url(r'^studyrecords/', customer.studyrecords, name='studyrecords'),
    # url(r'^addStudyRecords/', customer.addeditStudyRecords, name='addstudyrecords'),
    # url(r'^editStudyRecords/(\d+)/', customer.addeditStudyRecords, name='editstudyrecords'),
    # url(r'^deleteStudyRecords/(\d+)/', customer.deleteStudyRecords, name='deletestudyrecords'),
    # url(r'^bulkdeletestudy/', customer.bulkdeletestudy, name='bulkdeletestudy'),
    # 课程记录展示
    url(r'^courserecord/', customer.CourseRecord.as_view(),name='courserecord'),
    # 学习记录展示
    url(r'^studyrecord/(\d+)/', customer.StudyRecord.as_view(), name='studyrecord'),






]
