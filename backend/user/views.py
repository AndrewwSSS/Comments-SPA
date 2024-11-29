import json

import jwt
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from django.shortcuts import get_object_or_404

from user.serializers import (
    CreateUserSerializer,
    CustomTokenObtainPairSerializer
)

from pubsub.pub import RabbitMQProducer
from user.models import User
from user.tokens import (
    generate_email_verification_token,
    verify_verification_token
)


class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = generate_email_verification_token(
                {"id": user.id, "email": user.email}
            )
            user_publisher = RabbitMQProducer()
            user_publisher.publish_user_acc_activation(
                json.dumps({"id": user.id, "token": token})
            )
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class EmailVerificationView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def get(request):
        token = request.GET.get("token")
        if not token:
            return Response(
                {"message": "Token is missing"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payload = verify_verification_token(
                token
            )
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation link expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_id = payload.get("id")
        if not user_id:
            return Response(
                {"message": "Invalid token payload"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)
        if not user.is_active:
            user.is_active = True
            user.save()
            user_publisher = RabbitMQProducer()
            user_publisher.publish_new_active_user(
                json.dumps({"id": user.id})
            )
            return Response(
                {"message": "User account is active successfully."},
                status=status.HTTP_200_OK
            )
        return Response(
            {"message": "User account is already activated"},
            status=status.HTTP_200_OK
        )
