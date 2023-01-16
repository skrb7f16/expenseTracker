from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse  
from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate  
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .tokens import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
class Signup(APIView):
    def get(self,request,format=None):
        return Response({"msg":"Wrong Endpoint"},status=400)
    
    def post(self,request):
        username=request.data['username']
        password=request.data['password']
        email=request.data['email']
        first_name=request.data['first_name']
        last_name=request.data['last_name']
        current_site = get_current_site(request) 
        user=User(username=username,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.is_active=False
        user.save()
        message = render_to_string('emailFormat.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            }) 
        emailM=EmailMessage("activation link ",message,to=[email])
        emailM.send()
        return Response({"msg":"email has been sent please confirm your identity to get token"})


@api_view(['GET'])
def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return Response({"msg":"Authentication successful please use username and password to get token key"},status=201)
    else:  
        return Response({'msg':'Activation link is invalid!'},status=400)

class UpdateUser(APIView):
    def post(self,request):
        user=request.user
        change=User.objects.filter(username=user.username)[0]
        change.first_name=request.data['first_name']
        change.last_name=request.data['last_name']
        change.username=request.data['username']
        change.email=request.data['email']
        change.set_password(request.data['password'])
        change.save()
        return Response({"msg":"updated"},status=201)
