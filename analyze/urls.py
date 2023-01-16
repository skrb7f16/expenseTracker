from django.urls import path
from .views import AnalyzerPerMonth,AnalyzerPerYear,AnalyzeLastWeek
urlpatterns=[
    path('/totalPerMonth',AnalyzerPerMonth.as_view()),
    path('/totalPerYear',AnalyzerPerYear.as_view()),
    path('/lastWeek',AnalyzeLastWeek.as_view())
]