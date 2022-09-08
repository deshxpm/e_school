from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import (CourseGroup, Course, Faculty, Student,
                     Category, SubCategory, Notes,Video_Lecture,
                     Ratings, CourseOverview,VideoTesting,FrequentlyAskQuestion,ContactForm,InternshipForm,Transaction
                     )

# Register your models here.
admin.site.register(CourseGroup)

admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Category)
admin.site.register(Notes)
admin.site.register(SubCategory)
admin.site.register(Ratings)

admin.site.register(CourseOverview)

# admin.site.register(Video_Lecture)


admin.site.register(FrequentlyAskQuestion)
admin.site.register(ContactForm)


admin.site.register(InternshipForm)
admin.site.register(Transaction)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','price_','members','is_active','faculty_name')
    list_filter = ('price','category','sub_category',)
    search_fields = ('name__startswith',)

    def price_(self,current_course):
        return format_html("<b><i>{}</i></b>",int(current_course.price))


    def faculty_name(self,current_course):
        return str(current_course.faculty.user.first_name)+" "+str(current_course.faculty.user.last_name)

    # def videos(self,current_course):
    #     number_of_videos_=current_course.video_lectures.count()
    #     # url = (
    #     #         reverse("admin:core_person_changelist")
    #     #         + "?"
    #     #         + urlencode({"courses__id": f"{current_course.id}"})
    #     # )
    #     # return format_html('<a href="{}">{} Videos</a>', url, number_of_videos_)
    #     return number_of_videos_
    # def notes(self,current_course):
    #     number_of_pdf=current_course.notes_un.count()
    #     return number_of_pdf

    def members(self,current_course):
        members =current_course.member.count()
        return members

    # videos.short_description = "Videos"
    members.short_description = "Members"
    # notes.short_description = "Notes"

@admin.register(Video_Lecture)
class VideosAdmin(admin.ModelAdmin):
    list_display = ('name','course_',)
    list_filter = ('course',)

    def course_(self,obj):
        associate_course=obj.course
        # url=(
        #     reverse("admin:classroom_course_changelist")
        #     +"?"+urlencode({"video_lecture__id":{obj.id}})
        # )
        url=f"http://127.0.0.1:8000/admin/classroom/course/{associate_course.id}/change/"
        return format_html('<a href="{}">{}</a>',url,associate_course.name)

# admin/classroom/course/3/change/
