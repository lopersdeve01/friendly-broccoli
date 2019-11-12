
# django外部文件使用django环境
import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IGnb.settings")
    import django
    django.setup()


    import random
    from sales import models


    sex_type = (('male', '男性'), ('female', '女性')) #

    source_type = (('qq', "qq群"),
                   ('referral', "内部转介绍"),
                   ('website', "官方网站"),
                   ('baidu_ads', "百度推广"),
                   ('office_direct', "直接上门"),
                   ('WoM', "口碑"),
                   ('public_class', "公开课"),
                   ('website_luffy', "路飞官网"),
                   ('others', "其它"),)
    course_choices = (('LinuxL', 'Linux中高级'),
                      ('PythonFullStack', 'Python高级全栈开发'),)




    print(random.choice(sex_type))
    obj_list = []
    for i in range(251):
        obj = models.Customer(
            qq=f"{i+1}236798",
            name=f'liye{i}',
            sex=random.choice(sex_type)[0],
            source=random.choice(source_type)[0],
            course=random.choice(course_choices)[0],

        )
        obj_list.append(obj)

    models.Customer.objects.bulk_create(obj_list)




















