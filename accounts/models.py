from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator,MaxValueValidator,MaxLengthValidator

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):

		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):

		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin     = True
		user.is_staff     = True
		user.is_superuser = True

		user.save(using=self._db)
		return user





class Account(AbstractBaseUser):

	email 		 = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 	 = models.CharField(max_length=30, unique=True)
	date_joined	 = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login	 = models.DateTimeField(verbose_name='last login', auto_now=True)


	# All these field are required for custom user model
	is_admin	 = models.BooleanField(default=False)
	is_active	 = models.BooleanField(default=True)
	is_staff	 = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	# other
	first_name   = models.CharField(max_length=30,blank=True,null=True)
	last_name    = models.CharField(max_length=30,blank=True,null=True)
	# phone_number = PhoneNumberField(default='1234567890')
	phone_number = models.IntegerField(default='1234567890',validators=[
																		MinValueValidator(1000000000),
																		MaxValueValidator(9999999999)
																		])
	profile_pic = models.ImageField(blank=True,null=True,upload_to='Profile_Pics',default='media/profile')
	# we have to add here some at least 10 default images

	is_verify    = models.BooleanField(default=False)

	USERNAME_FIELD  = 'email'   # This with login with email
	REQUIRED_FIELDS = ['username']  # other than email

	objects= MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

class StaticData(models.Model):

	index             = models.IntegerField(default="For Chronological Order")
	email_address_0   = models.EmailField(verbose_name="email", max_length=60,blank=True,null=True)
	email_address_1   = models.EmailField(verbose_name="email", max_length=60,blank=True,null=True)
	facebook_handler  = models.URLField(blank=True,null=True)
	twitter_handler   = models.URLField(blank=True,null=True)
	instagram_handler = models.URLField(blank=True, null=True)
	linkedin_handler  = models.URLField(blank=True, null=True)
	phone_number      = models.IntegerField(default='1234567890', validators=[
		MinValueValidator(1000000000),
		MaxValueValidator(9999999999)
	])
	use               = models.BooleanField(default=False)


	def __str__(self):
		return str(self.index)


class NewslettersSubscribers(models.Model):
	email=models.EmailField(verbose_name="email", max_length=60, unique=True)

	def __str__(self):
		return str(self.email)

