from django.urls import path
from .views import ExpensesView
urlpatterns=[
    path('',ExpensesView.as_view(),name="expencesAddOrList")
]