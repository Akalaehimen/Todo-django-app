from todos.models import *
from todos.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from todos.utils import validate_email


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Extract registration data from serializer
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            password = serializer.validated_data['password']  

            
            if not validate_email(serializer.validated_data['email']):
                return Response({"message": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create user with provided data
            user = CustomUserManager.objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password  # Pass password to create_user method
            )
            
            # Additional logic as needed
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         request.data['username'] = request.data['username'].lower()
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key,
#                          'email': user.email
#                          })


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)

#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response(
#             {"message": "Logout successful"},
#             status=status.HTTP_200_OK)



