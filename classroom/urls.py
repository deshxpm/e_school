from django.urls import path
from classroom import views


urlpatterns = [
	path('', views.index, name='home'),
	path('course_list/',views.courseListView,name='course_list'),
	path('course/<slug>',views.courseDetailView ,name='course_detail'),


	#ToDO Course Creation
	path('course/add_videos/<course_slug>',views.addVideosToCourse ,name='add_videos_to_course'),
	path('course/add_notes/<course_slug>',views.addNotesToCourse ,name='add_notes_to_course'),
	path('create_course/',views.createCourse,name='create_course'),

	#Static Pages
	path('contact_us/',views.contactUs,name="contact_us"),
	path('about_us/',views.aboutUs,name="about_us"),

	path('internships/',views.internships,name='internships'),
	path('internships/<id>',views.internshipDetail,name='internships-detail'),

	# checkout page
	path('checkout/<course_slug>',views.checkoutPage,name="checkout"),

	#user course
	path('purchase_course/',views.user_courseListView,name='purchase_course'),

	#course-detail-view-for-member
	path('course/purchased/<course_slug>/',views.course_detail_view_for_purchase_user,name='course-access'),
	path('course/purchased/<course_slug>/videos',views.course_videos_for_purchase_user,name='course_videos_for_purchase_user'),
	path('course/purchased/<course_slug>/notes',views.course_notes_for_purchase_user,name='course_notes_for_purchase_user'),

	path('course/checkout/<course_slug>', views.checkout, name='paytmcheckout'),
	path('course/handlerequest/<course_slug>/<username>', views.handlerequest, name='handlerequest'),

]


"""
====== Server Task ======

3. Google Auth

====== Backend Task =======

1. redirection ( done with login redirection but register redirection is remain due OTP verification)
2. courses list page categories
3. email auth/otp
6. password change fields
7. in classroom/notes model add proper path and file name in media folder , check save() method
8. like blog post
10. redirect messages / alert messages 
11. default profile pic



====== Frontend Task =======

1. Blog Detail Page   
2. Profile Page  
3. Content
4. Active Button On Navbar Home
5. Mobile View Profile DropDown
6. Course Access Page Separated Notes And Videos
7. reduce margin of course list,register ,login pages 
8. add profile icon in navbar 
9. profile settings page
11. profile edit page
10 . In course detail page backgro

"""

#todo
# python manage.py loaddata db.json
# if you added some data or change anything in models.py
# python manage.py dumpdata > db.json

