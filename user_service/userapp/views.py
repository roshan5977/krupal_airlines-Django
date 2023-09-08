from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from django.contrib.auth import authenticate
from .models import User
from rest_framework import status
import jwt
import datetime
import logging
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from django.contrib.auth.models import User
import random
from django.contrib.auth.hashers import make_password
User = get_user_model()

logger = logging.getLogger(__name__)


def authorizeUser(token, role):
    # token = request.headers.get('Authorization')
    # role=request.headers.get('role')
    if not token:
        raise AuthenticationFailed("Not Authorized")
    token = token.split('Bearer ')[1:]
    if not token:
        raise AuthenticationFailed("Invalid token")
    token = token[0]
    try:
        payload = jwt.decode(token, "secret", algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Not Authorized')


# Register
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Login


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)
        logger.info(user)
        if not user:
            raise AuthenticationFailed('Incorrect email or password!')

        payload = {
            'email': user.email,
            'role': user.role,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        user_details = User.objects.get(email=email)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            # Include serialized user details
            'user': UserSerializer(user_details).data
        }
        return response

# User Details


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(email=payload['id']).first()
        print(user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

# Get all Emails


class GetAllUsersEmail(GenericAPIView, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        try:
            response = self.list(request)
            user_emails = [user['email'] for user in response.data]
            return Response(user_emails)
        except Exception as e:
            logger.exception("An error occurred while getting all user emails")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Get all Users
class GettingAllUsers(GenericAPIView, ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        token = request.headers.get('Authorization')
        role = request.headers.get('role')
        authorizeUser(token, role)
        try:
            return self.list(request)
        except Exception as e:
            logger.exception("An error occurred while getting all users")

# Update User


class UpdateUser(GenericAPIView, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, **kwargs):
        try:
            return self.update(request, **kwargs)
        except Exception as e:
            logger.exception(
                "An error occurred while update a user: %s", str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# Delete User


class DeleteUser(GenericAPIView, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, **kwargs):
        try:
            return self.destroy(request, **kwargs)
        except Exception as e:
            logger.exception("An error occurred while delete the user: %s")
            print("id is not there")

# Get By Id


class GetById(GenericAPIView, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, **kwargs):
        try:
            return self.retrieve(request, **kwargs)
        except Exception as e:
            logger.exception("An error occurred while getting a user By Id")

# Forgot password


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=400)

        otp = random.randint(1000, 9999)
        logger.info(f'OTP: {otp}')  # Log the OTP value for debugging purposes

        # Send OTP to user's email
        subject = 'Password Reset OTP'
        message = f'Your OTP for password reset is: {otp}'
        from_email = 'sarudr06@gmail.com'
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email,
                      recipient_list, fail_silently=False)
            logger.info('OTP sent successfully')
            return Response({'message': 'OTP sent successfully.', 'Secretkey': otp+12345})
        except Exception as e:
            logger.error(f'Failed to send OTP: {e}')
        return Response({'message': 'Failed to send OTP.'}, status=500)

# ChangePassword


class ChangePassword(APIView):
    def put(self, request, id):
        try:
            user = User.objects.get(user_id=id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        new_password = request.data.get('new_password')
        if new_password:
            user.password = make_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=200)
        else:
            return Response({'error': 'New password not provided'}, status=400)

# New password


class newpassword(APIView):
    def put(self, request, email):
        try:
            user = User.objects.get(email=email)
        except:
            return Response({'error': 'User not found'}, status=404)
        new_password = request.data.get('password')
        if new_password:
            user.password = make_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=200)
        else:
            return Response({'error': 'New password not provided'}, status=400)

# Get By Email


class GetByEmail(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        return User.objects.get(email=email)


# class LoginView(APIView):
#     def post(self, request):
#         data = request.data
#         email = data.get('email')
#         password = data.get('password')

#         user = authenticate(email=email, password=password)
#         if not user:
#             raise AuthenticationFailed('Incorrect email or password!')

#         access_token = AccessToken.for_user(user)

#         user_details = User.objects.filter(email=email)

#         response = Response()
#         response.data = {
#             'access_token': str(access_token),
#             'user': UserSerializer(user_details).data  # Include serialized user details
#         }
#         return response


# class LogoutView(APIView):
#     def post(self, request):
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             'message': 'success'
#         }
#         return response
