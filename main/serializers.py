from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BookingData

class UserSerializer(serializers.ModelSerializer):
    '''
    To serialize/deserialize username and password obtained from 
    signup and login api request.
    '''
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user


class BookingDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingData
        fields = ['name', 'phone_number', 'seats', 'booked_date']
