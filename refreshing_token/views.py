from rest_framework.views import APIView
from refreshing_token.util import generate_token_pair, refresh_access_token
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class GenerateTokenPair(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username,password=password)
        if user is None:
            return Response(data={"error":"no user found with provided username and password"},status=status.HTTP_401_UNAUTHORIZED)
        
        token_pair = generate_token_pair(user)

        return Response(data=token_pair)  

class Verify(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        return Response(data={"yep its working"})

class RefreshTokenView(APIView):
    
    def post(self,request):
        refresh_token = request.data.get("refresh_token")
        access_token = refresh_access_token(refresh_token=refresh_token)

        return Response(data={"access_token":access_token})


