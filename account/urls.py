from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path('register/', registration_view, name="register"),
    path('child-register/', child_registration_view, name="child-register"),
	path('login/', login_view, name="login"),
	path('logout/', logout_view, name="logout"),
	path('profil/',profile, name='profil'),
    path('saved/',saved, name='saved'),
    path('down/', down, name="down"),
    path('up/', up, name="up"),
    path('history/', history, name="history"),
    path('code-confirmation/', confirmcode, name="confirmcode"),
    path('mettre-a-niveau/',upgrade, name='upgrade'),
	path('profil/<user>',userprofile, name='userprofil'),

    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), 
        name='password_change_complete'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url="/"), name='password_reset_confirm'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html',
  email_template_name='password_reset_email.html',success_url='/password_reset/done'), name='password_reset'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
     name='password_reset_complete'),
]
