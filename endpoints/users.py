from todos.models import *
from todos.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from todos.utils import validate_email, validate_password


# class RegisterView(APIView):
#     permission_classes = (AllowAny,)

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             # Extract registration data from serializer
#             email = serializer.validated_data['email']
#             username = serializer.validated_data['username']
#             first_name = serializer.validated_data['first_name']
#             last_name = serializer.validated_data['last_name']
#             password = serializer.validated_data['password']  

            
#             if not validate_email(serializer.validated_data['email']):
#                 return Response({"message": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
            
#             # Create user with provided data
#             # user = CustomUserManager.objects.create_user(
#             #     email=email,
#             #     username=username,
#             #     first_name=first_name,
#             #     last_name=last_name,
#             #     password=password  # Pass password to create_user method
#             # )
            
#             # Additional logic as needed
            
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
            
            # check if the user is providing a valid email
            if not validate_email(serializer.validated_data['email']):
                return Response({"message": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
            

            # Check if email already exists
            if get_user_model().objects.filter(email=email).exists():
                return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
            
             # Check if username already exists
            if get_user_model().objects.filter(username=username).exists():
                return Response({"message": "Username is already Taken"}, status=status.HTTP_400_BAD_REQUEST)
            
            # check if the user meets the criteria for the password
            if not validate_password(serializer.validated_data['password']):
                return Response({"message": "   Ensure your password contains uppercase, lowercase, special character and is up to 6"}, status=status.HTTP_400_BAD_REQUEST)

            # Create user with provided data
            user = get_user_model().objects.create_user(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            
            # Additional logic as needed
            
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # Extract login data from request
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login user
            login(request, user)
            
            # Generate or retrieve token
            token, _ = Token.objects.get_or_create(user=user)
            
            # Return token and user data
            return Response({'token': token.key, 'user': UserSerializer(user).data}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)




class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Check if the user has an authentication token
        try:
            token = Token.objects.get(user=request.user)
        except Token.DoesNotExist:
            return Response(
                {"message": "User is not authenticated with a token"},
                status=status.HTTP_400_BAD_REQUEST)

        # Delete the authentication token
        token.delete()
        
        return Response(
            {"message": "Logout successful"},
            status=status.HTTP_200_OK)

class DeleteUserView(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)