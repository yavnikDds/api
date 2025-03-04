from rest_framework.decorators import api_view # Imports DRF’s decorator to mark a function as an API endpoint.
from rest_framework.response import Response # Imports DRF’s Response class to send JSON data.
from rest_framework import status
from .serializers import UserSerializer,LoginSerializer

@api_view(['GET']) #Decorator that restricts this endpoint to GET requests.
def hello_world(request): #Defines a function (view) that takes a request object (data from the client).
    return Response ({"message": "Hello, World!"}) #Returns a JSON response with a key message and value Hello, World!.

@api_view(['POST'])    
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered!"}, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        return Response({"message":f"Welcome, {user.fullname}!"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



