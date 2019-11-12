import copy

from sales import models
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from sales import myforms
from utils.page import DQPage
from django.conf import settings
from django.db.models import Q
from django.views import View
# Create your views here.

def home(request):
    return render(request,'customer/home.html')


class Customers(View):
    def get(self,request):
        print(request.get_full_path())  #/customers/?page=3
        path = request.path
        recv_data = copy.copy(request.GET)
        current_page_number = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据   陈
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
                       'search_field': search_field})
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

        from django.db import transaction
        with transaction.atomic():
            customer_list = models.Customer.objects.select_for_update().filter(id__in=cids, consultant__isnull=True)
            user_obj = models.UserInfo.objects.get(username=request.session.get('username'))
            customer_list.update(consultant_id=user_obj.id)

        if customer_list.count() != len(cids):

            # return HttpResponse('回家练手速吧!!!')
            return render(request, 'customer/customers.html',
                          {'errors':'错误是什么,,,,'})




    def reverse_sg(self,request,cids):
        customer_list = models.Customer.objects.filter(id__in=cids, consultant__isnull=True)
        customer_list.update(consultant=None)


def addEditCustomer(request,n=None):
    old_obj = models.Customer.objects.filter(pk=n).first()

    # if old_obj not in models.Customer.objects.filter(consultant__isnull=True):
    #     return HttpResponse('已经处于别人了')
    # old_obj = models.Customer.objects.filter(pk=n)

    label  = '编辑页面' if n else '添加页面'

    if request.method == 'GET':

        book_form_obj = myforms.CustomerModelForm(instance=old_obj)
        return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})

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
            return render(request, 'customer/editcustomer.html', {'book_form_obj': book_form_obj,'label':label})


class ConsultRecord(View):

    def get(self,request):
        recv_data = copy.copy(request.GET)
        current_page_number = request.GET.get('page')  # 当前页码
        search_field = request.GET.get('search_field')  # 搜索条件
        keyword = request.GET.get('keyword')  # 搜索数据   陈

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
                       'search_field': search_field})

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
    old_obj = models.ConsultRecord.objects.filter(pk=n).first()
    label  = '编辑页面' if n else '添加页面'

    if request.method == 'GET':
        record_form_obj = myforms.ConsultRecordModelForm(request,instance=old_obj)
        return render(request, 'consult_record/add_edit_consult_record.html', {'record_form_obj': record_form_obj,'label':label})

    else:
        next_path = request.GET.get('next')
        record_form_obj = myforms.ConsultRecordModelForm(request,request.POST,instance=old_obj)

        if record_form_obj.is_valid():
            record_form_obj.save()

            return redirect('sales:consultrecords') if not n else redirect(next_path)
        else:
            return render(request, 'consult_record/add_edit_consult_record.html', {'record_form_obj': record_form_obj,'label':label})


# 报名信息展示
def enrollments(request):

    if request.method == 'GET':

        enrollments_obj = models.Enrollment.objects.all()

        return render(request,'customer/enrollment.html',{'enrollments_obj':enrollments_obj})




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


from django.forms.models import modelformset_factory
from django import forms

class StudyRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.StudyRecord
        fields = '__all__'


class StudyRecord(View):

    def get(self,request,course_id):
        formset_obj = modelformset_factory(model=models.StudyRecord,form=StudyRecordModelForm,extra=0)
        # formset = formset_obj()
        formset = formset_obj(queryset=models.StudyRecord.objects.filter(course_record_id=course_id))
        # all_study_records = models.StudyRecord.objects.filter(course_record_id=course_id)
        # return render(request,'customer/study_record.html',{'all_study_records':all_study_records})
        return render(request,'customer/study_record.html',{'formset':formset})

    def post(self,request,course_id):
        formset_obj = modelformset_factory(model=models.StudyRecord, form=StudyRecordModelForm, extra=0)
        formset = formset_obj(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(request.path)
        else:
            return render(request, 'customer/study_record.html', {'formset': formset})

