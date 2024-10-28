from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import CreateUserSerializer


class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
