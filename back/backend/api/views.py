from .models import Product
from .serializers import ProductSerializer
from rest_framework import viewsets
from typing import Any, Optional
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import parsers, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login
from .models import User
from .renderers import UserJSONRenderer
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
   RegistrationSerializer,
   LoginSerializer,
   LogoutSerializer,
   UserSerializer,
)




class RegistrationAPIView(APIView):
   permission_classes = (AllowAny,)
   renderer_classes = (UserJSONRenderer,)
   serializer_class = RegistrationSerializer

   def post(self,request: Request) -> Response:
        #instanciating the serializer with the user object passed from the frontend request
        #so the returned data will always be in a user obj
        user_request = request.data.get('user',{}) #returning an empty object if key pair user not found in dict
        serializer = self.serializer_class(data=user_request)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        
        
        return Response(
            #inside the Response.user there will be the get_tokens data as well (cuz its part of the serializer)
            serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    
    def post(self, request:Request) -> Response:
        user = request.data.get('user', {})
        
        serializer = self.serializer_class(data=user)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    lookup_url_kwarg = 'id'
    parser_classes = [
        parsers.JSONParser,
        parsers.FormParser,
        parsers.MultiPartParser,
    ]

    def get(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        #request has a user object passed in the axios call
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        #getting the user object passed in the request
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(request.user, data=serializer_data, partial=True)

        if serializer.is_valid():

            user = serializer.save()

            return Response(UserSerializer(user).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
   
    def get_serializer_context(self):
        return {"request": self.request}
  
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self,request,*args,**kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)