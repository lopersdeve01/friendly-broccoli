#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
import requests
from bs4 import BeautifulSoup

response = requests.get(
    url='http://fontawesome.dashgame.com/',
)

response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, 'html.parser')
web = soup.find(attrs={'id': 'web-application'})

icon_list = []

for item in web.find_all(attrs={'class': 'fa-hover'}):
    tag = item.find('i')  #i标签
    class_name = tag.get('class')[1]  #fa fa-map-pin
    # icon_list.append([class_name, f'{"fa"+ str(tag)}'])
    icon_list.append([f'{"fa "+  class_name }',str(tag)])
    # print('tag',tag)
    # print('class_name',class_name)
    # print('class_name1',f'{"fa " + class_name }')
    # for i in icon_list:
    #     print(i[0], i[1])

print('icon_list',icon_list)
