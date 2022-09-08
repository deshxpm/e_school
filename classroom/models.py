import datetime
import string

from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from .choices import *
import random
from django.core.validators import MaxValueValidator, MinValueValidator

# Signals
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.utils import timezone,dates
from datetime import date


from embed_video.fields import EmbedVideoField



from django.conf import settings

User=settings.AUTH_USER_MODEL




class VideoTesting(models.Model):
	name = models.CharField(max_length=10)
	url  = EmbedVideoField()


class Faculty(models.Model):
	# faculty_name = models.CharField(max_length=255)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user.username)


class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	active_status = models.CharField(max_length=255)

	def __str__(self):
		return str(self.user.username)


class Category(models.Model):
	thumbnail=models.ImageField(upload_to="category_thumbnail",blank=True,null=True)
	desc = models.CharField(max_length=100,default="Category Desc")
	category_name = models.CharField(max_length=255)

	def __str__(self):
		return str(self.category_name)


class SubCategory(models.Model):
	category_name = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
	sub_category_name = models.CharField(max_length=255)

	def __str__(self):
		return str(self.sub_category_name)


class Notes(models.Model):
	index    = models.IntegerField(help_text="For Chronological Order", blank=True, null=True,unique=True)
	name     = models.CharField(help_text="Name OF PDF File",blank=True,null=True,max_length=20)
	document = models.FileField(upload_to='documents/')
	thumbnail= models.ImageField(upload_to="notes_thumbnail",blank=True,null=True)
	course = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return str(self.document)


class Video_Lecture(models.Model):
	index     = models.IntegerField(help_text="For Chronological Order",blank=True,null=True,unique=True)
	name      = models.CharField(help_text="Add Name OF Video",blank=True,null=True,max_length=20)
	thumbnail = models.ImageField(upload_to="videos_thumbnail", blank=True, null=True)
	course    = models.ForeignKey('Course',on_delete=models.CASCADE,blank=True,null=True)
	video_url = EmbedVideoField(blank=True,null=True)

	def __str__(self):
		return str(self.index)+str(self.name)



def generate_random_string():
	length = 6
	while True:
		code = ''.join(random.choices(string.ascii_uppercase , k=length))
		if Course.objects.filter(code=code).count() == 0:
			break
	return code


class Course(models.Model):
	name           = models.CharField(max_length=255)
	category       = models.ForeignKey(Category,    on_delete=models.CASCADE,blank=True,null=True)
	sub_category   = models.ForeignKey(SubCategory, on_delete=models.CASCADE,blank=True,null=True)
	faculty        = models.ForeignKey(Faculty,     on_delete=models.CASCADE,blank=True,null=True)

	small_desc     = models.CharField(max_length=500,blank=True,null=True,help_text="Add small descriptions over here")
	description    = models.TextField(blank=True, null=True)
	price          = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
	discount_price = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)

	code           = models.CharField(max_length=20, default=generate_random_string)

	thumbnail 		= models.ImageField(upload_to="course_thumbnail", blank=True, null=True)
	date_of_created = models.DateTimeField(default=timezone.now(),blank=True,null=True)
	slug           = models.SlugField(max_length=250,blank=True,null=True,unique=True,help_text="This the slug field remain it empty")
	is_active      = models.BooleanField(default=True)
	is_completed   = models.BooleanField(default=True)
	is_live        = models.BooleanField(default=False)
	is_like        = models.ManyToManyField(User,blank=True,related_name='likes')
	is_save        = models.ManyToManyField(User,blank=True,related_name='saves')

	member         = models.ManyToManyField(User,blank=True,related_name='course_purchase')


	# un neseccery fields
	video_lectures = models.ManyToManyField(Video_Lecture, blank=True, help_text="Ignore It",related_name="video_lectures_IgnoreIt")
	course_overview = models.ManyToManyField('CourseOverview', blank=True, help_text="Ignore It",related_name="course_overview_IgnoreIt")
	notes_un = models.ManyToManyField(Notes, blank=True, help_text="Ignore It", related_name="course_notes_IgnoreIt")
	students = models.ManyToManyField(Student, blank=True)

	def __str__(self):
		return str(self.name)

	# def save(self, *args, **kwargs):
	# 	if not self.id:
	# 		super(Course, self).save(*args, **kwargs)
	# 		string_ = ''.join(random.choices(string.ascii_lowercase, k=6))
	# 		num_ = random.randint(1000, 9999)
	#
	# 		self.slug = slugify(self.name) + "-" + str(string_) + "-" + str(num_)
	# 		super(Course, self).save(*args, **kwargs)

	def get_course_absolute_url(self):
		return reverse('course_detail',kwargs={'slug':self.slug})


"""SLUG Field"""

def pre_save_course_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		string_ = ''.join(random.choices(string.ascii_lowercase, k=6))
		num_ = random.randint(1000, 9999)
		instance.slug = slugify(instance.name) + "-" + str(string_) + "-" + str(num_)

pre_save.connect(pre_save_course_receiver, sender=Course)



class CourseGroup(models.Model):
	course_name = models.CharField(max_length=20, blank=True, null=True)
	students = models.ManyToManyField(Student)
	faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.course_name)


class CourseOverview(models.Model):
	index = models.IntegerField(help_text="For Chronological Order", blank=True, null=True, unique=True)
	title = models.CharField(max_length=100,blank=True,null=True,default="CourseOverview")
	text = models.TextField(blank=True,null=True)
	course = models.ForeignKey('Course', on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return str(self.index)+" "+str(self.title)

# class BuyCourse(models.Model):
# 	user   = models.ForeignKey(User,on_delete=models.CASCADE)
# 	course = models.ForeignKey(Course,on_delete=models.CASCADE)
#





class Ratings(models.Model):
	course_title = models.CharField(max_length=255)
	description = models.TextField()

	def no_of_ratings(self):
		ratings = Total_Ratings.objects.filter(user_ratings=self)
		return len(ratings)

	def avg_rating(self):
		sum = 0
		ratings = Total_Ratings.objects.filter(user_ratings=self)
		for ratings in ratings:
			sum += ratings.stars
		if len(ratings) > 0:	
			return sum / len(ratings)
		else:
			return 0



class Total_Ratings(models.Model):
	user_ratings = models.CharField(max_length=20, blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	def __str__(self):
		return str(self.user_ratings)	
	# def average(self):
	# 	print("hello")
	# 	total = self.user_ratings
	# 	print(total)
	# 	return (total/len(user_ratings))


class FrequentlyAskQuestion(models.Model):
	index = models.IntegerField(help_text="For Chronological Order", blank=True, null=True, unique=True)
	question = models.CharField(max_length=500, blank=True, null=True, default="How long is this course duration")
	answer = models.TextField(blank=True, null=True)

	def __str__(self):
		return str(self.index)+"."+str(self.question)


class ContactForm(models.Model):
	name=models.CharField(max_length=100)
	email = models.EmailField(verbose_name="email", max_length=60)
	phone_number = models.IntegerField(default='1234567890', validators=[
		MinValueValidator(1000000000),
		MaxValueValidator(9999999999)
	])
	message=models.TextField(help_text="Type Your Message here")

	def __str__(self):
		return str(self.name)

class InternshipForm(models.Model):
	name=models.CharField(max_length=200,default="The Python Developer")
	company_name=models.CharField(max_length=200,default="InternYuva")
	role = models.CharField(max_length=200,default="Django Developer")
	author=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL)
	url= models.URLField(blank=True,null=True)
	start_date = models.DateField(default=date.today(), blank=True, null=True, help_text="yyyy-mm-dd")
	end_date = models.DateField(default=date.today() + datetime.timedelta(days=60), blank=True, null=True,help_text="yyyy-mm-dd")
	desc = models.TextField(blank=True,null=True)
	stipend = models.IntegerField(default=4000)
	is_list  = models.BooleanField(default=True)
	is_reviewed=models.BooleanField(default=False)

	def __str__(self):
		return str(self.name)

	def get_duration(self):
		months=self.end_date.day-self.start_date.day
		return months//30


class Transaction(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	order_id = models.AutoField(primary_key=True)
	item_json = models.TextField()
	course = models.ForeignKey(Course,on_delete=models.CASCADE)
	amount = models.IntegerField(default=0)
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	mobile = models.CharField(max_length=255)

	def _str_(self):
		return str(self.order_id)+" "+str(self.course.name)


