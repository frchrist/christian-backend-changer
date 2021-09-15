from rest_framework import permissions



class IsOwner(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        print(obj)
        return obj.client == request.user


class HasVerifiedEmail(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        return obj.client.email_is_valid == True
