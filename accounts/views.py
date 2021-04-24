import json

from django import http
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic import View, FormView

from accounts.forms import LoginForm
from utils.response import BadRequestJsonResponse, MethodNotAllowedJsonResponse, \
    UnauthorizedJsonResponse, ServerErrorJsonResponse
from .serializers import UserSerializer, UserProfileSerializer
from .forms import RegisterForm


def user_login(request):
    """ 用户登录 """
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            form.do_login(request=request)
            print('表单验证通过')
            return redirect(to='/accounts/user/info')
        else:
            print(form.errors)
    else:
        form = LoginForm()
    return render(request, 'user_login.html', {
        'form': form
    })


@login_required
def user_info(request):
    """ 用户信息 """
    print(request.user)
    return render(request, 'user_info.html')


def user_logout(request):
    """ 用户退出登录 """
    logout(request=request)
    return redirect(to='/accounts/user/info')


def user_api_login(request):
    """ 用户登录接口——POST """
    # 获取输入内容
    if request.method == 'POST':
        # 表单验证
        form = LoginForm(request.POST)
        # 如果通过验证，执行登录
        if form.is_valid():
            user = form.do_login(request=request)
            # 返回内容：用户信息
            profile = user.profile
            data = {
                'user': UserSerializer(obj=user).to_dict(),
                'profile': UserProfileSerializer(obj=profile).to_dict(),
            }
            return http.JsonResponse(data=data)
        else:
            # 如果未通过表单验证，返回错误信息
            err = json.loads(form.errors.as_json())
            return BadRequestJsonResponse(err)
    else:
        # 请求方式不被允许
        return MethodNotAllowedJsonResponse()


def user_api_logout(request):
    """ 用户登出接口"""
    logout(request=request)
    return http.HttpResponse(status=201)


class UserDetailView(View):
    """ 用户详细信息接口 """
    def get(self, request):
        # 获取用户信息
        user = request.user
        # 是否为游客
        if not user.is_authenticated:
            # 返回401状态码
            return UnauthorizedJsonResponse()
        else:
            # 返回用户详细信息
            profile = user.profile
            data = {
                'user': UserSerializer(obj=user).to_dict(),
                'profile': UserProfileSerializer(obj=profile).to_dict(),
            }
            return http.JsonResponse(data=data)


class UserRegisterView(FormView):
    """ 用户注册接口 """
    form_class = RegisterForm
    http_method_names = ['post']

    def form_valid(self, form):
        """ 表单通过验证 """
        result = form.do_register(request=self.request)
        if result is not None:
            user, profile = result
            data = {
                'user': UserSerializer(obj=user).to_dict(),
                'profile': UserProfileSerializer(obj=profile).to_dict(),
            }
            return http.JsonResponse(data=data, status=201)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):
        """ 表单未通过验证 """
        err_list = json.loads(form.errors.as_json())
        return http.JsonResponse(data=err_list)
