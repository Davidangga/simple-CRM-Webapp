from django.shortcuts import redirect
from django.http import HttpResponse
# create decorator meaning create function before another fucntion is excuted
def unautheticated_user(view_func):
    def wrapper_func(request,*args,**kwargs): # def untuk fungsi yang di akses terlebi dahulu
        if request.user.is_authenticated:
            return redirect('manage:dashboard')
        else:
            return view_func(request,*args,**kwargs) #return viewfunc berarti mengkakses fungsi di bawah decorator
    return wrapper_func

def allowed_users(allowed_roles = []): # cuman boleh allow user sesual roles yang di kasih in
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request,*args,**kwargs)

            else:
                return HttpResponse("You are not authorized to view this page")
                
        return wrapper_func
    return decorator

def Admin_only(view_func): #decorators to allow user yang berasal dari group admin
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'Customer':
            return redirect('manage:user-page')
        
        if group == 'Admin':
            return view_func(request,*args,**kwargs)
        
    return wrapper_func

