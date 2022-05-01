from django.contrib.auth.models import User as auth_user
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserProfile, UserBudget
from .serializers import UserSerializer, UserProfileSerializer, UserBudgetSerializer
from rest_framework.renderers import JSONRenderer


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
        profile, created = UserProfile.objects.update_or_create(
            user=request.user,
            defaults={
                "name": profile_info["name"],
                # interests=profile_info["interests"],
                # hobbies=profile_info["hobbies"],
                "age": profile_info["age"],
                "gender": profile_info["gender"],
                "net_worth": profile_info["net_worth"]}
        )
        profile.save()
        return Response({
            "status": "200",
        })


class UserBudgetAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        # if UserBudget.objects.deleted(name=request.user.username).exists():
        #     return Response({
        #         "status": "404",
        #     })
        # else:

        budget = UserBudget.objects.get(user=request.user)
        serializer = UserBudgetSerializer(budget)
        return Response(JSONRenderer().render(serializer.data))

    def post(self, request, *args, **kwargs):
        budget_info = request.data
        budget, created = UserBudget.objects.update_or_create(
            user=request.user,
            defaults={"budget": budget_info["budget"]})
        budget.save()
        return Response({
            "status": "200",
        })

    def delete(self, request, *args, **kwargs):
        budget = UserBudget.objects.get(user=request.user)
        budget.delete()
        return Response({
            "status": "200",
        })


class UserBudgetRetrieveAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        user_name = request.data["username"]
        retrieved_object = UserBudget.objects(user=user_name)
        if retrieved_object.deleted:
            retrieved_object.restore()
            return Response({
                "status": "200",
                "message": "instance restored"
            })
        else:
            retrieved_object.delete()
            return Response({
                "message": "instance already restored",
            })


class UserAdminAPI(APIView):
    def delete(self, request, *args, **kwargs):
        user = auth_user.objects.get(username=request.data["username"])
        user.delete()
        return Response({
            "status": "200",
            "message": "User deleted",
        })
