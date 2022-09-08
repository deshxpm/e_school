from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # url(r'^accounts/change/password/$', changepassword, name='changepassword'),
    # url(r'^accounts/forgot/password/$', forgotpassword, name='forgotpassword'),
    # path('',views.index,name='home'),
    path('register/',views.registration_view,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('login/',views.login_view,name='login'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='password_reset'),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html')
         , name='password_reset_confirm'),
    path('password-reset-complete',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),

    # path('verification/',views.verification,name='otp_verification'),

    path('register_with_js_form/',views.registration_with_js_form,name="register_with_js_form"),

    path('profile-edit/',views.updateProfile,name='update-profile')
]
