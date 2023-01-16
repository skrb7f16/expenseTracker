from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Expenses,Categories
from .serializers import CategorySerializer,ExpenseSerializer
# Create your views here.

class ExpensesView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        expenses=Expenses.objects.filter(by=request.user)
        seri=ExpenseSerializer(expenses,many=True)
        return Response(seri.data,status=200)

    def post(self,request):
        category=Categories.objects.filter(title=request.data['category'])[0]
        expense=Expenses(amount=request.data['amount'],by=request.user,title=request.data['title'],category=category)
        expense.save()
        return Response({"msg":"Saved"},status=201)


