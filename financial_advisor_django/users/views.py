from django.contrib.auth.models import User as auth_user
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserProfile, UserBudget
from .serializers import UserSerializer, UserProfileSerializer, UserBudgetSerializer
from .permissions import AdviserPermission
from rest_framework.renderers import JSONRenderer
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


class TopTenUsersAPI(GenericAPIView, ListModelMixin):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['fields'] = self.fields

        return serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.user = request.user

        if kwargs.get('mk') == 'profiles':
            self.serializer_class = UserProfileSerializer
            model = UserProfile
            self.fields = ['name', 'net_worth', 'age']
        elif kwargs.get('mk') == 'budgets':
            self.serializer_class = UserBudgetSerializer
            model = UserBudget
            self.fields = ['budget', 'modified']
        else:
            pass
        # still works when using only kwargs instead of self.kwargs but not work outside of the get method
        start = self.kwargs.get('sk')
        end = self.kwargs.get('ek')
        if not(start and end):
            self.queryset = model.objects.filter(
                user__in=auth_user.objects.order_by('budget__budget'))[:4]
        else:
            filters = {}
            filters['budget__budget__gte'] = start
            filters['budget__budget__lte'] = end
            self.queryset = model.objects.filter(
                user__in=auth_user.objects.filter(**filters))
        if AdviserPermission().has_permission(self, request):
            return self.list(request, *args, **kwargs)
        else:
            query = model.objects.filter(user=request.user)
            serializer = self.get_serializer(query, many=True)
            #self.serializer_class(query, fields=self.fields)
            return JsonResponse(serializer.data, safe=False)
