from django.urls import path
from .views import AnalyzerPerMonth,AnalyzerPerYear
urlpatterns=[
    path('/totalPerMonth',AnalyzerPerYear.as_view())
]