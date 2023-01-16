from rest_framework import serializers
from .models import Categories,Expenses,User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password','email','first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CategorySerializer(serializers.Serializer):
    title=serializers.CharField(max_length=255)
    at=serializers.DateTimeField()
    class Meta:
        model=Categories
        fields="__all__"

class ExpenseSerializer(serializers.Serializer):
    category=CategorySerializer(many=False)
    by=UserSerializer(many=False)
    title=serializers.CharField(max_length=255)
    amount=serializers.FloatField()
    at=serializers.DateTimeField()
    atDate=serializers.DateField()
    class Meta:
        model=Expenses
        fields="__all__"
    



