from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models.functions import ExtractMonth,ExtractIsoYear
from expences.models import Expenses
from expences.serializers import ExpenseSerializer
import datetime as dt
from django.utils import timezone
import datetime
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

class AnalyzerPerYear(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response({"msg","hello invalid request"},status=400)
    
    def post(self,request):
        if request.data['year']==None:
            return Response({"msg":"please provide a target month and year"},status=400)
        year=int(request.data['year'])
        month=int(request.data['month'])
        expences=Expenses.objects.filter(by=request.user).filter(atDate__gte=dt.date(year-1,month,1)).filter(atDate__lte=dt.date(year,month,31))
        result={}
        for i in expences:
            print(i)
            temp1=str(i.atDate).split('-')[1]
            temp2=str(i.atDate).split('-')[0]
            if(result.get(temp1+'-'+temp2)==None):
                result[temp1+"-"+temp2]=0
            result[temp1+"-"+temp2]+=i.amount

            
        # seri=ExpenseSerializer(expences,many=True)
        return Response(result,status=200)    
    
        
class AnalyzeLastWeek(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        curr=datetime.datetime.today()
        start=curr-datetime.timedelta(days=7)
        start=start.date()
        curr=curr.date()

        expenses=Expenses.objects.filter(by=request.user).filter(atDate__gte=start).filter(atDate__lte=curr)
        # seri=ExpenseSerializer(expenses,many=True)
        results={}
        for i in expenses:
            if results.get(str(i.atDate))==None:
                results[str(i.atDate)]=[]
            temp=ExpenseSerializer(i)
            results[str(i.atDate)].append(temp.data)
        return Response(results,status=200)
        