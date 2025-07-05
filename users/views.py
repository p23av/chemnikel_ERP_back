from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView
from .utils import decode_token
from .models import User
from .serializers import (
    CompleteRegistrationSerializer,
    UserSerializer,
    CreateUserSerializer,
    ChangePasswordSerializer,
    WhoAmISerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
import logging
logger = logging.getLogger(__name__)


class MeView(APIView):
    authentication_classes = [JWTAuthentication]
    """Возвращает информацию о текущем пользователе"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"[DEBUG] request.user: {request.user}")
        if not request.user or request.user.is_anonymous:
            return Response({"detail": "User is not authenticated"}, status=401)
        
        serializer = WhoAmISerializer(request.user)
        return Response(serializer.data)


class CreateUserView(generics.CreateAPIView):
    """Создание нового пользователя (владельцем или менеджером)"""
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChangePasswordView(APIView):
    """Смена пароля текущим пользователем"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({'old_password': 'Неверный пароль'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'status': 'Пароль успешно изменён'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteRegistrationView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        email = request.data.get("email")

        if not all([token, new_password, confirm_password, email]):
            return Response({"detail": "Missing data."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"detail": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = decode_token(token)
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.email = email
        user.is_active = True
        user.save()

        return Response({"detail": "Registration completed successfully."}, status=status.HTTP_200_OK)
    
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Только для авторизованных

class LogoutView(APIView):
  def post(self, request):
    try:
      refresh_token = request.data["refresh"]
      token = RefreshToken(refresh_token)
      token.blacklist()  # Добавляем в черный список
      return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
      return Response(status=status.HTTP_400_BAD_REQUEST)
        
