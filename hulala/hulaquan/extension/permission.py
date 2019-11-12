
from rest_framework.permissions import BasePermission


class LuffyPermission(BasePermission):
    print('LuffyPermission')
    message = {"status":False,"error":"登录成功之后才能评论"}
    def has_permission(self, request, view):
        print('request.method',request.method)
        print('request.data.get("username")',request.data.get('username'))
        print('request.user',request.user)
        if request.method == "GET":
            return True
        else:
            # request.method == "POST":
            if request.user:
                return True
        return False
