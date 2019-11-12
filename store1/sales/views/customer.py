import copy
from sales import models
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from sales import myforms
from utils.page import DQPage
from django.conf import settings
from django.db.models import Q
from django.views import View

from django.db import transaction
from django.forms.models import modelformset_factory
from django import forms
import time
# Create your views here.




def home(request):
    username = request.session.get('username')
    # time = Datetime.now()
    return render(request,'customer/home.html',{'username':username})


class Customers(View):
    def get(self,request):
        print(request.get_full_path())  #/customers/?page=3
        path = request.path
        recv_data = copy.copy(request.GET)
        current_page_number = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据   陈
        username=request.session.get('username')
        if keyword:
            q = Q()  # 实例化q对象
            q.children.append([search_field, keyword])  #
            all_customers = models.Customer.objects.filter(q)
        else:
            all_customers = models.Customer.objects.all()

        if path == reverse('sales:customers'):
            # 筛选所有公户的客户信息
            tag = '1'
            all_customers = all_customers.filter(consultant__isnull=True)
        else:
            tag = '0'
            all_customers = all_customers.filter(consultant__username=request.session.get('username'))

        total_count = all_customers.count()
        per_page_count = settings.PER_PAGE_COUNT
        page_number_show = settings.PAGE_NUMBER_SHOW
        page_obj = DQPage(current_page_number, total_count, per_page_count, page_number_show, recv_data)
        all_customers = all_customers[page_obj.start_data_number:page_obj.end_data_number]
        page_html = page_obj.page_html_func()
        return render(request, 'customer/customers.html',
                      {'tag': tag, 'all_customers': all_customers, 'page_html': page_html, 'keyword': keyword,
                       'search_field': search_field,'username':username})
    def post(self,request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')  # 选中的客户的

        # customer_list = models.Customer.objects.filter(id__in=cids,consultant__isnull=True)

        if hasattr(self,action):
            ret = getattr(self,action)(request,cids)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你的方法不对!!')
    def bulk_delete(self,request,cids):
        customer_list = models.Customer.objects.filter(id__in=cids, consultant__isnull=True)
        customer_list.delete()
        return redirect(request.path)

    def reverse_gs(self,request,cids):
        with transaction.atomic():
            customer_list = models.Customer.objects.select_for_update().filter(id__in=cids, consultant__isnull=True)
        if customer_list.count() != len(cids):
            return HttpResponse('回家练手速吧!!!')

        user_obj = models.UserInfo.objects.get(username=request.session.get('username'))
        customer_list.update(consultant_id=user_obj.id)

    def reverse_sg(self,request,cids):
        customer_list = models.Customer.objects.filter(id__in=cids, consultant__isnull=True)
        customer_list.update(consultant=None)


def addEditCustomer(request,n=None):
    username = request.session.get('username')
    old_obj = models.Customer.objects.filter(pk=n).first()
    label  = '编辑页面' if n else '添加页面'

    if request.method == 'GET':

        book_form_obj = myforms.CustomerModelForm(instance=old_obj)
        return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label,'username':username})

    else:

        next_path = request.GET.get('next')  #
        print(next_path) # http://127.0.0.1:8000/editcustomer/116/?next=/customers/?search_field=qq__contains&keyword=1&page=4
        # /customers/?search_field=qq__contains
        # /customers/?search_field=qq__contains&keyword=1&page=4
        book_form_obj = myforms.CustomerModelForm(request.POST,instance=old_obj)

        if book_form_obj.is_valid():
            book_form_obj.save()
            return redirect(next_path)
        else:
            return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label,'username':username})


class ConsultRecord(View):

    def get(self,request):
        recv_data = copy.copy(request.GET)
        current_page_number = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据   陈
        username=request.session.get('username')

        # 单个客户的id值
        customer_id = request.GET.get('customer_id')

        # 查询逻辑
        if keyword:
            q = Q()  # 实例化q对象
            q.children.append([search_field, keyword])  #
            all_records = models.ConsultRecord.objects.filter(q)
        else:
            all_records = models.ConsultRecord.objects.all()



        all_records = all_records.filter(consultant__username=request.session.get('username'),delete_status=False)

        if customer_id:
            all_records = all_records.filter(customer_id=customer_id)

        total_count = all_records.count()

        per_page_count = settings.PER_PAGE_COUNT
        page_number_show = settings.PAGE_NUMBER_SHOW
        page_obj = DQPage(current_page_number, total_count, per_page_count, page_number_show, recv_data)
        all_records = all_records[page_obj.start_data_number:page_obj.end_data_number]

        page_html = page_obj.page_html_func()

        return render(request, 'consult_record/consult_record.html',
                      {'all_records': all_records, 'page_html': page_html, 'keyword': keyword,
                       'search_field': search_field,'username':username})

    def post(self,request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')  # 选中的客户的

        consult_record_list = models.ConsultRecord.objects.filter(id__in=cids)

        if hasattr(self,action):
            ret = getattr(self,action)(request,consult_record_list)
            if ret:
                return ret
            else:
                return redirect(request.path)
        else:
            return HttpResponse('你的方法不对!!')

    def bulk_delete(self,request,consult_record_list):
        # customer_list.delete()
        consult_record_list.update(delete_status=True)
        return redirect(request.path)



# 添加和编辑跟进记录
def addEditConsultRecord(request,n=None):
    username = request.session.get('username')
    old_obj = models.ConsultRecord.objects.filter(pk=n).first()
    label  = '编辑页面' if n else '添加页面'

    if request.method == 'GET':
        record_form_obj = myforms.ConsultRecordModelForm(request,instance=old_obj)
        return render(request, 'consult_record/add_edit_consult_record.html', {'record_form_obj': record_form_obj,'label':label,'username':username})
    else:

        next_path = request.GET.get('next')
        record_form_obj = myforms.ConsultRecordModelForm(request,request.POST,instance=old_obj)

        if record_form_obj.is_valid():
            record_form_obj.save()

            return redirect('sales:consultrecords') if not n else redirect(next_path)
        else:
            return render(request, 'consult_record/add_edit_consult_record.html', {'record_form_obj': record_form_obj,'label':label,'username':username})



class Enrollment(forms.ModelForm):
    class Meta:
        model=models.Enrollment
        fields='__all__'
        # labels={'enrolled_date':'报名日期','customer':'客户名称','school':'所在校区','enrolment_class':'所报班级'}
        # widgets={'enrolled_date':forms.DateInput(attrs={'type':'date'}),'customer':forms.TextInput(attrs={'type':'text'}),
        #          'school':forms.TextInput(attrs={'type':'text'}),'enrolment_class':forms.TextInput(attrs={'type':'text'})}
        # error_messages={'enrolled_date':{'required':'not null'},'customer':{'required':'not null'},'enrolment_class':{'required':'not null'},'school':{'required':'not null'},}

def enrollmentrecord(request):
    username = request.session.get('username')
    search_field = request.GET.get('search_field')
    keyword = request.GET.get('keyword')
    if keyword:
        obj = models.Enrollment.objects.filter(**{search_field: keyword})
    else:
        obj=models.Enrollment.objects.all()
    return render(request,'enrollment_record/enrollment_record.html',{'obj':obj,'username':username})


def addEditEnrollmentRecord(request,n=None):
    username = request.session.get('username')
    print(n)
    label='添加记录' if not n else '编辑记录'
    old_obj = models.Enrollment.objects.filter(pk=n).first()
    if request.method == 'GET':
        obj = Enrollment(instance=old_obj)
        return render(request,'enrollment_record/add_edit_enroll_record.html',{'obj':obj,'label':label,'username':username})
    else:
        if not n:
           obj = Enrollment(request.POST)
           print(request.POST)
           obj.save()
           return redirect('sales:enrollmentrecords')
        else:
           obj = Enrollment(request.POST,instance=old_obj)
           if obj.is_valid():
               print(request.POST)
               obj.save()
               return redirect('sales:enrollmentrecords')
           else:
               # print(obj)
               return render(request, 'enrollment_record/add_edit_enroll_record.html', {'obj': obj,'username':username})

        #
        # next_path = request.GET.get('next')
        # obj =Enrollment(request, request.POST, instance=old_obj)
        # if obj.is_valid():
        #     obj.save()
        #     return redirect('sales:enrollmentrecords') if not n else redirect(next_path)
        # else:
        #     return render(request, 'enrollment_record/enrollment_record.html',
        #                   {'obj': obj})


def deleteEnrollmentRecord(request,n=None):
    if not n:
        nids=request.POST.getlist('mark')
        print(nids)
        models.Enrollment.objects.filter(pk__in=nids).update(delete_status=True)
    else:
        models.Enrollment.objects.filter(pk=n).update(delete_status=True)
    return redirect('sales:enrollmentrecords')

def bulkdelete(request):
    nids = request.GET.getlist('mark')
    print(nids)
    models.Enrollment.objects.filter(pk__in=nids).update(delete_status=True)
    return redirect('sales:enrollmentrecords')


# class Study(forms.ModelForm):
#     class Meta:
#         model=models.StudyRecord
#         fields='__all__'
#         labels={'student':'学员','course_record':'课程','attendance':'考勤','date':'日期','score':'成绩',}
#         # widgets={'enrolled_date':forms.DateInput(attrs={'type':'date'}),'customer':forms.TextInput(attrs={'type':'text'}),
#         #          'school':forms.TextInput(attrs={'type':'text'}),'enrolment_class':forms.TextInput(attrs={'type':'text'})}
#         # error_messages={'enrolled_date':{'required':'not null'},'customer':{'required':'not null'},'enrolment_class':{'required':'not null'},'school':{'required':'not null'},}
#
#
# # def studyrecords(request):
# #     username = request.session.get('username')
# #     search_field = request.GET.get('search_field')
# #     keyword = request.GET.get('keyword')
# #     if keyword:
# #         obj = models.StudyRecord.objects.filter(**{search_field: keyword})
# #     else:
# #         obj=models.StudyRecord.objects.all()
# #     return render(request,'studyrecord/studyrecords.html', {'obj':obj,'username':username})
# #
# #
# #
# # def addeditStudyRecords(request,n=None):
# #     username = request.session.get('username')
# #     label='添加记录' if not n else '编辑记录'
# #     old_obj = models.StudyRecord.objects.filter(pk=n).first()
# #     print(old_obj)
# #     if request.method == 'GET':
# #         obj = Study(instance=old_obj)
# #         print(obj)
# #         return render(request,'studyrecord/add_edit_record.html',{'obj':obj,'label':label,'username':username})
# #     else:
# #         if not n:
# #            obj = Study(request.POST)
# #            print(request.POST)
# #            obj.save()
# #            return redirect('sales:studyrecords')
# #         else:
# #            obj = Study(request.POST,instance=old_obj)
# #            if obj.is_valid():
# #                print(request.POST)
# #                obj.save()
# #                return redirect('sales:studyrecords')
# #            else:
# #                # print(obj)
# #                return render(request,'studyrecord/add_edit_record.html', {'obj': obj,'username':username})
# #
# #
# # def deleteStudyRecords(request,n=None):
# #     if not n:
# #         nids=request.POST.getlist('mark')
# #         print(nids)
# #         models.StudyRecord.objects.filter(pk__in=nids).update(delete_status=True)
# #     else:
# #         models.StudyRecord.objects.filter(pk=n).update(delete_status=True)
# #     return redirect('sales:studyrecords')
# #
# # def bulkdeletestudy(request):
# #     nids = request.GET.getlist('mark')
# #     print(nids)
# #     models.StudyRecord.objects.filter(pk__in=nids).update(delete_status=True)
# #     return redirect('sales:studyrecords')
# #
# class CourseRecord(View):
#     def get(self,request):
#         obj=models.CourseRecord.objects.all()
#         return render(request,'studyrecord/course_record.html',{'obj':obj})
#     def post(self,request):
#         action=request.POST.get('action')
#         cids=request.POST.get('cids')
#         if hasattr(self,action):
#             ret=getattr(self,action)(request,cids)
#             # if ret:
#             #     return ret
#             # else:
#             return redirect('sales:courserecord')
#
# def bulk_create_studyrecords(self,request,cids):
#     course_record_list=models.CourseRecord.objects.filter(pk__in=cids)
#
#     for obj in course_record_list:
#         s_obj=obj.re_class.customer_set.all().exclude(status='unregistered')
#         # student_objs = course_record.re_class.customer_set.all().exclude(status='unregistered')
#         student_list = []
#         for i in s_obj:
#             sr_obj=models.StudyRecord.objects.create(
#                 course_record=obj,
#                 student=i
#             )
#             student_list.append(sr_obj)
#         models.StudyRecord.objects.bilk_create(student_list)
#
#
#
# from django.forms.models import modelformset_factory
# from django import forms
#
#
#
# class StudyRecordModelForm(forms.ModelForm):
#     class Meta:
#         model=models.StudyRecord
#         fields='__all__'
#         # labels = {'student': '学员', 'course_record': '课程', 'attendance': '考勤', 'date': '日期', 'score': '成绩', }
#         # widgets={'enrolled_date':forms.DateInput(attrs={'type':'date'}),'customer':forms.TextInput(attrs={'type':'text'}),
#         #          'school':forms.TextInput(attrs={'type':'text'}),'enrolment_class':forms.TextInput(attrs={'type':'text'})}
#         # error_messages={'enrolled_date':{'required':'not null'},'customer':{'required':'not null'},'enrolment_class':{'required':'not null'},'school':{'required':'not null'},}
# class StudyRecord(View):
#     def get(self,request,course_id):
#         formset_obj=modelformset_factory(model=models.StudyRecord,form=StudyRecordModelForm,)
#         formset=formset_obj(queryset=models.StudyRecord.objects.filter(courese_record_id=course_id))
#         return render(request,'studyrecord/studyrecords.html',{'formset':formset})
#     def post(self,request,course_id):
#         formset_obj=modelformset_factory(model=models.StudyRecord,form=StudyRecordModelForm,)
#         formset=formset_obj(request.POST)
#         if formset.is_valid():
#             formset.save()
#             return redirect(request.path)
#         else:
#             return render(request,'studyrecord/studyrecords.html',{'formset':formset})


class CourseRecord(View):

    def get(self,request):

        course_records = models.CourseRecord.objects.all()

        return render(request,'customer/course_record.html',{'course_records':course_records})

    def post(self,request):
        action = request.POST.get('action')
        cids = request.POST.getlist('cids')

        if hasattr(self,action):
            getattr(self,action)(request,cids)
            # if ret:
            #     return ret
            # else:
            return redirect('sales:courserecord')

    # 批量创建学习记录
    def bulk_create_studyrecords(self,request,cids):

        course_record_list = models.CourseRecord.objects.filter(pk__in=cids)

        for course_record in course_record_list:
            student_objs = course_record.re_class.customer_set.all().exclude(status='unregistered')
            # for student in student_objs:
            #     models.StudyRecord.objects.create(
            #         course_record = course_record,
            #         student = student,
            #     )
            student_list = []
            for student in student_objs:
                obj = models.StudyRecord(
                    course_record = course_record,
                    student = student,
                )
                student_list.append(obj)

            models.StudyRecord.objects.bulk_create(student_list)




class StudyRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'


class StudyRecord(View):

    def get(self,request,course_id):
        formset_obj = modelformset_factory(model=models.StudyRecord,form=StudyRecordModelForm,extra=0)
        # formset = formset_obj()
        formset = formset_obj(queryset=models.StudyRecord.objects.filter(course_record_id=course_id))
        print(formset)
        # all_study_records = models.StudyRecord.objects.filter(course_record_id=course_id)
        # return render(request,'customer/study_record.html',{'all_study_records':all_study_records})
        return render(request,'customer/study_record.html',{'formset':formset})

    def post(self,request,course_id):
        formset_obj = modelformset_factory(model=models.StudyRecord, form=StudyRecordModelForm, extra=0)
        formset = formset_obj(request.POST)
        # print(request.POST)
        # print(formset)
        if formset.is_valid():
            formset.save()
            return redirect(request.path)
        else:
            return render(request, 'customer/study_record.html', {'formset': formset})

