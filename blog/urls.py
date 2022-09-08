from django.urls import path
from blog import views


urlpatterns = [
	path('', views.blog_home,name='blog_home'),
	path('post/<id>/',views.post_Details,name='blog_details'),
	path('post_create/',views.createPost,name='blog_create'),
	path('post_update/<id>/',views.updatePost,name='blog_update'),
	path('post_dalete/<id>/',views.delete_post,name='blog_delete'),
	path('add_intetnship/',views.add_internShip,name='add_internship')
]

# TODO

