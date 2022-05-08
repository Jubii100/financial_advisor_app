import requests
from django.contrib.auth.models import User as auth_user
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, UserBudget
from .serializers import UserProfileSerializer, UserBudgetSerializer, UserSerializer
from .permissions import AdviserPermission
from django.http import JsonResponse


class UserCreateAPI(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        user_creditentials = request.data
        user = auth_user.objects.create_user(
            username=user_creditentials["username"], password=user_creditentials["password"])
        user.save()
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username
        })


class LoginAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        user_creditentials = request.data
        user = auth_user.objects.get(
            username=user_creditentials["username"])
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username
        })


class LogOutAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        Token.objects.filter(user=request.user).delete()
        return Response({"message": "Logged out"})


class ExternalAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        results = self.request.query_params.get('type')
        response = {}
        r = requests.get(
            'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo')
        r_status = r.status_code

        if r_status == 200:
            response = r.json()

        else:
            response['status'] = r.status_code
            response['message'] = 'error'

        return Response(response)


class UserProfileUpdateAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        profile_info = request.data
        profile, created = UserProfile.objects.update_or_create(
            user=request.user,
            defaults={
                "name": profile_info["name"],
                "interests": profile_info["interests"],
                "hobbies": profile_info["hobbies"],
                "age": profile_info["age"],
                "gender": profile_info["gender"],
                "net_worth": profile_info["net_worth"]}
        )
        profile.save()

        return Response({
            "status": "200",
        })

    def get(self, request, *args, **kwargs):

        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        budget = UserProfile.objects.get(user=request.user)
        budget.delete()

        return Response({
            "status": "200",
        })


class UserBudgetAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):

        budget = UserBudget.objects.get(user=request.user)
        serializer = UserBudgetSerializer(budget)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        budget_info = request.data
        amount, created = UserBudget.objects.update_or_create(
            user=request.user,
            defaults={"amount": budget_info["amount"]})
        amount.save()

        return Response({
            "status": "200",
        })

    def delete(self, request, *args, **kwargs):
        budget = UserBudget.objects.get(user=request.user)
        budget.delete()

        return Response({
            "status": "200",
        })


class TopTenUsersAPI(GenericAPIView, ListModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer_class = UserSerializer
        kwargs['fields'] = ['profile', 'budget', 'username']

        return serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.user = request.user

        if AdviserPermission().has_permission(self, request):

            self.queryset = auth_user.objects.order_by(
                '-budget__amount').select_related('profile', 'budget')[:10]

            return self.list(request, *args, **kwargs)

        else:

            self.queryset = auth_user.objects.filter(
                budget__user=request.user).select_related('profile', 'budget')

            return self.list(request, *args, **kwargs)


class BudgetRangeAPI(GenericAPIView, ListModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer_class = UserSerializer
        kwargs['fields'] = ['profile', 'budget', 'username']

        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = request.user

        if AdviserPermission().has_permission(self, request):

            range_info = request.data

            try:
                min = range_info["min"]
            except:
                min = None
            try:
                max = range_info["max"]
            except:
                max = None

            filters = {}

            if min:

                filters['budget__amount__gte'] = min

            if max:

                filters['budget__amount__lte'] = max

            if filters:

                self.queryset = auth_user.objects.all().select_related(
                    'profile', 'budget').filter(**filters)

            else:

                return Response({
                    "status": "200",
                    "message": "No range applied"
                })

            return self.list(request, *args, **kwargs)

        else:

            self.queryset = auth_user.objects.filter(
                budget__user=request.user).select_related('profile', 'budget')

            return self.list(request, *args, **kwargs)
