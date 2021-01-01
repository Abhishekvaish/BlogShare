from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from PIL import Image

class UserManager(BaseUserManager):
	''' 
	it is mandatory to overwrite create_user and creat_super_user function 
	'''
	def create_user(self,email,first_name,last_name,password):
		if not email:
			raise ValueError("User must have an email")
		if not first_name:
			raise ValueError("User must have a first name")
		if not last_name:
			raise ValueError("User must have a last name")
		if not password:
			raise ValueError("User must have a password")

		user = self.model(
			email=self.normalize_email(email),
			first_name=first_name,
			last_name=last_name,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,first_name,last_name,password):
		user = self.create_user(
			email=email,
			first_name=first_name,
			last_name=last_name,
			password=password
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



class User(AbstractBaseUser):
	# custom fields  here
	email = models.EmailField(verbose_name='email',max_length=60,unique=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	img = models.ImageField(upload_to='images/',default='images/default.jpg')


	# these are compulsory fields
	date_joined	= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	# this tells django to use email as login field
	USERNAME_FIELD = 'email'
	# you don't need to add email to required field
	REQUIRED_FIELDS = ['first_name','last_name']

	# it specify which manager to use when a user is created
	objects = UserManager()

	def __str__(self):
		return f"User : {self.email}"


	# Compulsory functions
	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

	# overwriting custom save to resize image
	# def save(self,*args,**kwargs):
	# 	super(User,self).save(*args,**kwargs)
	# 	img_reshaped = Image.open(self.img.url)
	# 	#if img_reshaped.height > 225 or img_reshaped.width > 225:
	# 	img_reshaped =  img_reshaped.resize((225,225))
	# 	img_reshaped.save(self.img.path)

