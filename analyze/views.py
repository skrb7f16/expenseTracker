from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models.functions import ExtractMonth
from expences.models import Expenses
from expences.serializers import ExpenseSerializer
import datetime as dt
# Create your views here.



class AnalyzerPerMonth(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response({"msg","hello invalid request"},status=400)
    def post(self,request,format=None):
        if request.data['year']==None:
            return Response({"msg":"please provide a target month and year"},status=400)
        month=int(request.data['month'])
        if(month==None):month=1
        year=int(request.data['year'])
        end=year
        if(month==12):
            end=year+1
        expences=Expenses.objects.filter(by=request.user).filter(atDate__gte=dt.date(year,month,1)).filter(atDate__lte=dt.date(end,(month%12)+1,1))
        print(expences[0].atDate)
        seri=ExpenseSerializer(expences,many=True)
        return Response(seri.data,status=200)
        

        
