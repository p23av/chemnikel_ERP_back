from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# --- Кастомный менеджер пользователей ---
class UserManager(BaseUserManager):
    def create_user(self, username, full_name, role, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Логин обязателен")
        email = self.normalize_email(email)
        user = self.model(username=username, full_name=full_name, role=role, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, full_name, password=None):
        user = self.create_user(
            username=username,
            full_name=full_name,
            role='owner',
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# --- Кастомная модель пользователя ---
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('owner', 'Владелец'),
        ('manager', 'Менеджер'),
        ('worker', 'Работник'),
    ]

    # Логин (имя пользователя) — теперь используется вместо email
    username = models.CharField(max_length=150, unique=True)

    # Email — нужен для сброса пароля, но не обязателен сразу
    email = models.EmailField(unique=True, null=True, blank=True)

    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Активен ли пользователь (false = уволен)
    is_active = models.BooleanField(default=True)

    # Сотрудник ли пользователь (необходимое поле для Django админки)
    is_staff = models.BooleanField(default=False)

    # Обязательная привязка кастомного менеджера
    objects = UserManager()

    # --- Конфигурация логина ---
    # Указываем, что для логина используется username, а не email
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'full_name', 'role']

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"


