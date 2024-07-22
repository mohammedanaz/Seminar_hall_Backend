from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, BookingDataSerializer
from django.contrib.auth.models import User
from .models import BookingData
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404


def get_tokens_for_user(user):
    '''
    this function creates and return an object with access and refresh token.
    '''
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def login_view(request):
    '''
    Receives data and validate the credentials with user model instance and
    then creates tokens and serialized user data to send back.
    '''
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_404_NOT_FOUND)
    tokens = get_tokens_for_user(user)
    serializer = UserSerializer(instance=user)
    return Response({'tokens': tokens, 'user': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    '''
    Receives data and check for username existance. then validating the data and 
    creates a new instance in user model. then creates tokens and serialized user data 
    to send back. if received data not valid then response with 400 status code.
    '''
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        tokens = get_tokens_for_user(user)
        return Response({'tokens': tokens, 'user': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def fetch_booking(request):
    '''
    this view provides data from BookingData model in response to api calls. if any failure while 
    processing data , it response with 500 status code.
    '''
    try:
        if request.method == 'GET':
            bookings = BookingData.objects.all()
            serializer = BookingDataSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@api_view(['POST'])
@authentication_classes([SessionAuthentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_booking(request):
    '''
    this view creates new instance on BookingData model. before creating new instance
    it converts the field names (phoneNumber, bookedDate) from received data to match the field names
    of the model. if any failure while processing data , it response with 400 status code.
    '''
    data = request.data.copy()
    data['phone_number'] = data.pop('phoneNumber')
    data['booked_date'] = data.pop('bookedDate')
    serializer = BookingDataSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('invalid data')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['GET', 'HEAD'])
def ping_server(request):
    '''
    this view is only for making render server live.
    '''
    return Response({f'Ping recieved.'})
