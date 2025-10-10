from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, PublicUserSerializer

User = get_user_model()


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class PublicUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PublicUserSerializer(request.user)
        return Response(serializer.data)
