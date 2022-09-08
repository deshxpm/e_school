from django import forms
from .models import Course, Video_Lecture, Notes, CourseOverview


class CreateCourse(forms.ModelForm):
    class Meta:
        model=Course
        fields=['name','sub_category','price','thumbnail','is_active','is_completed','is_live']

class AddVideos(forms.ModelForm):
    class Meta:
        model=Video_Lecture
        fields=['index','name','video_url']

class AddNotes(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['index','name','document']


class AddCourseOverview(forms.ModelForm):
    class Meta:
        model=CourseOverview
        fields=['index','title','text']