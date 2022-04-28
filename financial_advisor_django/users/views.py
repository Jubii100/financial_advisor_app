from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User as auth_user
from django.shortcuts import render, get_object_or_404
from .forms import UserModelForm
from .forms import RegisterForm
from .models import UserProfile
from django.views.generic import (
    CreateView,
    DetailView,
    # ListView,
    UpdateView,
    # ListView,
    # DeleteView
)


# def test(request):
#    return render(request, 'users/test.html')


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

    @method_decorator(login_required(login_url='/login/'))
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

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get_success_url(self):
    #    return '/'

    # user = User.objects.create_user(username='john',
    #                                email='jlennon@beatles.com',
    #                                password='glass onion')
