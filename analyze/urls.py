from django.urls import path
from .views import AnalyzerPerMonth
urlpatterns=[
    path('/totalPerMonth',AnalyzerPerMonth.as_view())
]