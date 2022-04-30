from django.contrib.auth.models import User as auth_user
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile


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
