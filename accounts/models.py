from msilib.schema import Class
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings


# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('El usuario debe de tener un email')
        
        if not username:
            raise ValueError('El usuario debe tener un username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )

#guarda en la db
        user.set_password(password)
        user.is_admin = False
        user.is_active = False
        user.is_staff = False
        user.is_superadmin = False
        user.save(using=self._db)
        return user

#super usuario
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name
        )
# atribuciones del usuario como administrador
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user




#clase principal
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

#Campos atributos de django
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

#requisitos por email, nombre y apellido
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

#creamos la instancia de la clase para poder usarla
    objects =  MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
#se visualizara el email en admin django
    def __str__(self):
        return self.email
#solo si es admin tendra los permisos para hacer modificaciones
    def has_perm(self, perm, obj=None):
        return self.is_admin
# si es administrador super usuario que tenga permisos de editar los modulos y que retorne true
    def has_module_perms(self, add_label):
        return True
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    def __str__(self):
        return self.user.username

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'