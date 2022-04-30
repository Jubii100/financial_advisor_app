from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User as auth_user
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .forms import UserModelForm
from .forms import RegisterForm
from .models import UserProfile
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
)


class UserCreateAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        user_creditentials = request.data

        user = auth_user.objects.create_user(username=user_creditentials["username"],
                                             password=user_creditentials["password"])
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'username': user.username
        })


class UserProfileUpdateAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile_info = request.data
        profile, created = UserProfile.objects.update_or_create(name=profile_info["name"],
                                                                #    interests=profile_info["interests"],
                                                                #    hobbies=profile_info["hobbies"],
                                                                age=profile_info["age"],
                                                                gender=profile_info["gender"],
                                                                net_worth=profile_info["net_worth"],
                                                                user=request.user)
        profile.save()
        return Response('profile updated')


class UserCreateView(CreateView):
    template_name = 'users/user_create.html'
    form_class = RegisterForm
    # queryset = auth_user.objects.all()  # <blog>/<modelname>_list.html
    success_url = '/users/user_profile_update/'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    # def get_success_url(self):
    #    return '/'


class UserProfileDetailView(DetailView):
    template_name = 'users/user_detail_profile.html'
    queryset = UserProfile.objects.all().values(
        'name', 'interests', 'hobbies', 'age', 'gender', 'net_worth')

    def get_object(self):
        logedin_user = self.request.user
        return get_object_or_404(UserProfile, user=logedin_user)

    @ method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserProfileUpdateView(UpdateView):
    template_name = 'users/user_profile_update.html'
    form_class = UserModelForm
    queryset = UserProfile.objects.all().values(
        'name', 'interests', 'hobbies', 'age', 'gender', 'net_worth')  # <blog>/<modelname>_list.html

    def get_object(self):
        logedin_user = self.request.user
        return get_object_or_404(UserProfile, user=logedin_user)

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

    @ method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
