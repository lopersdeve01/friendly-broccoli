from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from api import models


# Create your views here.
class ServerView(APIView):
    def post(self,request,*args,**kwargs):
        print(request.data)
        return Response('发送成功')
    def get(self,request,*args,**kwargs):
        """ 返回今日未采集的服务器列表 """
        host_list = ["192.168.153.128","192.168.153.129","192.168.153.130"]
        return Response(host_list)
# data={'hostname': '192.168.153.128', 'info': {'memory': {'status': True, 'data': {'RAM slot #0': {'capacity': ' 1024 MB', 'slot': 'RAM slot #0', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #1': {'capacity': ' No Module Installed', 'slot': 'RAM slot #1', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #2': {'capacity': ' No Module Installed', 'slot': 'RAM slot #2', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #3': {'capacity': ' No Module Installed', 'slot': 'RAM slot #3', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #4': {'capacity': ' No Module Installed', 'slot': 'RAM slot #4', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #5': {'capacity': ' No Module Installed', 'slot': 'RAM slot #5', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #6': {'capacity': ' No Module Installed', 'slot': 'RAM slot #6', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #7': {'capacity': ' No Module Installed', 'slot': 'RAM slot #7', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #8': {'capacity': ' No Module Installed', 'slot': 'RAM slot #8', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #9': {'capacity': ' No Module Installed', 'slot': 'RAM slot #9', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #10': {'capacity': ' No Module Installed', 'slot': 'RAM slot #10', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #11': {'capacity': ' No Module Installed', 'slot': 'RAM slot #11', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #12': {'capacity': ' No Module Installed', 'slot': 'RAM slot #12', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #13': {'capacity': ' No Module Installed', 'slot': 'RAM slot #13', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #14': {'capacity': ' No Module Installed', 'slot': 'RAM slot #14', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #15': {'capacity': ' No Module Installed', 'slot': 'RAM slot #15', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #16': {'capacity': ' No Module Installed', 'slot': 'RAM slot #16', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #17': {'capacity': ' No Module Installed', 'slot': 'RAM slot #17', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #18': {'capacity': ' No Module Installed', 'slot': 'RAM slot #18', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #19': {'capacity': ' No Module Installed', 'slot': 'RAM slot #19', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #20': {'capacity': ' No Module Installed', 'slot': 'RAM slot #20', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #21': {'capacity': ' No Module Installed', 'slot': 'RAM slot #21', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #22': {'capacity': ' No Module Installed', 'slot': 'RAM slot #22', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #23': {'capacity': ' No Module Installed', 'slot': 'RAM slot #23', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #24': {'capacity': ' No Module Installed', 'slot': 'RAM slot #24', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #25': {'capacity': ' No Module Installed', 'slot': 'RAM slot #25', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #26': {'capacity': ' No Module Installed', 'slot': 'RAM slot #26', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #27': {'capacity': ' No Module Installed', 'slot': 'RAM slot #27', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #28': {'capacity': ' No Module Installed', 'slot': 'RAM slot #28', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #29': {'capacity': ' No Module Installed', 'slot': 'RAM slot #29', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #30': {'capacity': ' No Module Installed', 'slot': 'RAM slot #30', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #31': {'capacity': ' No Module Installed', 'slot': 'RAM slot #31', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #32': {'capacity': ' No Module Installed', 'slot': 'RAM slot #32', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #33': {'capacity': ' No Module Installed', 'slot': 'RAM slot #33', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #34': {'capacity': ' No Module Installed', 'slot': 'RAM slot #34', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #35': {'capacity': ' No Module Installed', 'slot': 'RAM slot #35', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #36': {'capacity': ' No Module Installed', 'slot': 'RAM slot #36', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #37': {'capacity': ' No Module Installed', 'slot': 'RAM slot #37', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #38': {'capacity': ' No Module Installed', 'slot': 'RAM slot #38', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #39': {'capacity': ' No Module Installed', 'slot': 'RAM slot #39', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #40': {'capacity': ' No Module Installed', 'slot': 'RAM slot #40', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #41': {'capacity': ' No Module Installed', 'slot': 'RAM slot #41', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #42': {'capacity': ' No Module Installed', 'slot': 'RAM slot #42', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #43': {'capacity': ' No Module Installed', 'slot': 'RAM slot #43', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #44': {'capacity': ' No Module Installed', 'slot': 'RAM slot #44', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #45': {'capacity': ' No Module Installed', 'slot': 'RAM slot #45', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #46': {'capacity': ' No Module Installed', 'slot': 'RAM slot #46', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #47': {'capacity': ' No Module Installed', 'slot': 'RAM slot #47', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #48': {'capacity': ' No Module Installed', 'slot': 'RAM slot #48', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #49': {'capacity': ' No Module Installed', 'slot': 'RAM slot #49', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #50': {'capacity': ' No Module Installed', 'slot': 'RAM slot #50', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #51': {'capacity': ' No Module Installed', 'slot': 'RAM slot #51', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #52': {'capacity': ' No Module Installed', 'slot': 'RAM slot #52', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #53': {'capacity': ' No Module Installed', 'slot': 'RAM slot #53', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #54': {'capacity': ' No Module Installed', 'slot': 'RAM slot #54', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #55': {'capacity': ' No Module Installed', 'slot': 'RAM slot #55', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #56': {'capacity': ' No Module Installed', 'slot': 'RAM slot #56', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #57': {'capacity': ' No Module Installed', 'slot': 'RAM slot #57', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #58': {'capacity': ' No Module Installed', 'slot': 'RAM slot #58', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #59': {'capacity': ' No Module Installed', 'slot': 'RAM slot #59', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #60': {'capacity': ' No Module Installed', 'slot': 'RAM slot #60', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #61': {'capacity': ' No Module Installed', 'slot': 'RAM slot #61', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #62': {'capacity': ' No Module Installed', 'slot': 'RAM slot #62', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'RAM slot #63': {'capacity': ' No Module Installed', 'slot': 'RAM slot #63', 'model': 'DRAM', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #0': {'capacity': ' No Module Installed', 'slot': 'NVD #0', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #1': {'capacity': ' No Module Installed', 'slot': 'NVD #1', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #2': {'capacity': ' No Module Installed', 'slot': 'NVD #2', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #3': {'capacity': ' No Module Installed', 'slot': 'NVD #3', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #4': {'capacity': ' No Module Installed', 'slot': 'NVD #4', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #5': {'capacity': ' No Module Installed', 'slot': 'NVD #5', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #6': {'capacity': ' No Module Installed', 'slot': 'NVD #6', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #7': {'capacity': ' No Module Installed', 'slot': 'NVD #7', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #8': {'capacity': ' No Module Installed', 'slot': 'NVD #8', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #9': {'capacity': ' No Module Installed', 'slot': 'NVD #9', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #10': {'capacity': ' No Module Installed', 'slot': 'NVD #10', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #11': {'capacity': ' No Module Installed', 'slot': 'NVD #11', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #12': {'capacity': ' No Module Installed', 'slot': 'NVD #12', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #13': {'capacity': ' No Module Installed', 'slot': 'NVD #13', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #14': {'capacity': ' No Module Installed', 'slot': 'NVD #14', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #15': {'capacity': ' No Module Installed', 'slot': 'NVD #15', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #16': {'capacity': ' No Module Installed', 'slot': 'NVD #16', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #17': {'capacity': ' No Module Installed', 'slot': 'NVD #17', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #18': {'capacity': ' No Module Installed', 'slot': 'NVD #18', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #19': {'capacity': ' No Module Installed', 'slot': 'NVD #19', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #20': {'capacity': ' No Module Installed', 'slot': 'NVD #20', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #21': {'capacity': ' No Module Installed', 'slot': 'NVD #21', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #22': {'capacity': ' No Module Installed', 'slot': 'NVD #22', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #23': {'capacity': ' No Module Installed', 'slot': 'NVD #23', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #24': {'capacity': ' No Module Installed', 'slot': 'NVD #24', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #25': {'capacity': ' No Module Installed', 'slot': 'NVD #25', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #26': {'capacity': ' No Module Installed', 'slot': 'NVD #26', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #27': {'capacity': ' No Module Installed', 'slot': 'NVD #27', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #28': {'capacity': ' No Module Installed', 'slot': 'NVD #28', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #29': {'capacity': ' No Module Installed', 'slot': 'NVD #29', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #30': {'capacity': ' No Module Installed', 'slot': 'NVD #30', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #31': {'capacity': ' No Module Installed', 'slot': 'NVD #31', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #32': {'capacity': ' No Module Installed', 'slot': 'NVD #32', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #33': {'capacity': ' No Module Installed', 'slot': 'NVD #33', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #34': {'capacity': ' No Module Installed', 'slot': 'NVD #34', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #35': {'capacity': ' No Module Installed', 'slot': 'NVD #35', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #36': {'capacity': ' No Module Installed', 'slot': 'NVD #36', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #37': {'capacity': ' No Module Installed', 'slot': 'NVD #37', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #38': {'capacity': ' No Module Installed', 'slot': 'NVD #38', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #39': {'capacity': ' No Module Installed', 'slot': 'NVD #39', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #40': {'capacity': ' No Module Installed', 'slot': 'NVD #40', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #41': {'capacity': ' No Module Installed', 'slot': 'NVD #41', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #42': {'capacity': ' No Module Installed', 'slot': 'NVD #42', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #43': {'capacity': ' No Module Installed', 'slot': 'NVD #43', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #44': {'capacity': ' No Module Installed', 'slot': 'NVD #44', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #45': {'capacity': ' No Module Installed', 'slot': 'NVD #45', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #46': {'capacity': ' No Module Installed', 'slot': 'NVD #46', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #47': {'capacity': ' No Module Installed', 'slot': 'NVD #47', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #48': {'capacity': ' No Module Installed', 'slot': 'NVD #48', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #49': {'capacity': ' No Module Installed', 'slot': 'NVD #49', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #50': {'capacity': ' No Module Installed', 'slot': 'NVD #50', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #51': {'capacity': ' No Module Installed', 'slot': 'NVD #51', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #52': {'capacity': ' No Module Installed', 'slot': 'NVD #52', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #53': {'capacity': ' No Module Installed', 'slot': 'NVD #53', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #54': {'capacity': ' No Module Installed', 'slot': 'NVD #54', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #55': {'capacity': ' No Module Installed', 'slot': 'NVD #55', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #56': {'capacity': ' No Module Installed', 'slot': 'NVD #56', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #57': {'capacity': ' No Module Installed', 'slot': 'NVD #57', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #58': {'capacity': ' No Module Installed', 'slot': 'NVD #58', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #59': {'capacity': ' No Module Installed', 'slot': 'NVD #59', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #60': {'capacity': ' No Module Installed', 'slot': 'NVD #60', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #61': {'capacity': ' No Module Installed', 'slot': 'NVD #61', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #62': {'capacity': ' No Module Installed', 'slot': 'NVD #62', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}, 'NVD #63': {'capacity': ' No Module Installed', 'slot': 'NVD #63', 'model': 'Other', 'speed': 'Unknown', 'manufacturer': 'Not Specified', 'sn': 'Not Specified'}}, 'error': None}, 'nic': {'status': True, 'data': {'ens33': {'up': True, 'hwaddr': '00:0c:29:a7:25:33', 'inet': [{'address': '192.168.153.128', 'netmask': '255.255.255.0', 'broadcast': '192.168.153.255'}]}}, 'error': None}, 'disk': {'status': True, 'data': {'0': {'slot': '0', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5NV'}, '1': {'slot': '1', 'pd_type': 'SAS', 'capacity': '279.396', 'model': 'SEAGATE ST300MM0006     LS08S0K2B5AH'}, '2': {'slot': '2', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1SZNSAFA01085L     Samsung SSD 850 PRO 512GB               EXM01B6Q'}, '3': {'slot': '3', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF912433K     Samsung SSD 840 PRO Series              DXM06B0Q'}, '4': {'slot': '4', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAF303909M     Samsung SSD 840 PRO Series              DXM05B0Q'}, '5': {'slot': '5', 'pd_type': 'SATA', 'capacity': '476.939', 'model': 'S1AXNSAFB00549A     Samsung SSD 840 PRO Series              DXM06B0Q'}}, 'error': None}, 'board': {'status': True, 'data': {'manufacturer': 'VMware, Inc.', 'model': 'VMware Virtual Platform', 'sn': 'VMware-56 4d 0b a2 33 65 cc ad-58 1a 72 72 6f a7 25 33'}, 'error': None}}}
# d0=data['hostname']
# d1=data['info']['memory']
# d2=data['info']['nic']
# d3=data['info']['disk']
# d4=data['info']['board']

def query(request):
    # # 获取服务器的hostname保存到数据库，目的是自动解析
    # # 类似data1，data2，data3
    # # host_data={}
    # # 将多个字典加进列表，类似
    # # 循环列表
    # data_list = [data1, data2, data3~~~]
    # host_list=[]
    # for i in data_list:
    #     host_list.append({'hostname':i['hostname']})
    # print(host_list)
    # for j in host_list:
    #     models.Host.objects.create(**j)
    # # return HttpResponse('OK')
    #
    # # 在其他数据库添加内容，注意添加外键
    #
    #     # d1 = i['info']['memory']
    #
    #     obj=models.Host.objects.filter(hostname=i['hostname'])
    #     memory=i['info']['memory']['data']
    #     'RAM slot # 0': {'capacity': ' 1024 MB','slot': 'RAM slot #0','model': 'DRAM','speed': 'Unknown','manufacturer': 'Not Specified','sn': 'Not Specified'},
    #     'RAM slot  #1': {'capacity': ' No Module Installed','slot': 'RAM slot #1','model': 'DRAM','speed': 'Unknown','manufacturer': 'Not Specified','sn': 'Not Specified'},
    #     for k,v in memory.items():
    #         models.Memory.objects.create(**v, host=obj)
    #
    #
    #     data= {'capacity':'No Module Installed','slot': 'NVD #55','model': 'Other','speed': 'Unknown','manufacturer': 'Not Specified','sn': 'Not Specified'}
    #     models.Memory.objects.create(**data,host_id=1)
    #     # data={'hostname':'192.168.153.128'}
    #     # models.Host.objects.create(**data)

    return HttpResponse('OK')