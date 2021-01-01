from django.urls import path
from . import views
import django.contrib.auth.views as auth_views

urlpatterns = [
	path('',views.index,name='index'),
	
	path('register/',views.register,name='register'),

	path('activate/<uidb64>/<token>',views.activate, name='activate'),

	path('login/', auth_views.LoginView.as_view(template_name="user/login.html"),
	name='login'),

	path('logout/',auth_views.LogoutView.as_view(template_name="user/logout.html"),
	name='logout'),


	path('password_reset/',auth_views.PasswordResetView.as_view(
		template_name="user/password_reset.html"),name="password_reset"),

	path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(
	template_name="user/password_reset_done.html"),name="password_reset_done"),

	path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
	template_name="user/password_reset_confirm.html",success_url="/password_reset_complete")
	,name="password_reset_confirm"),

	path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
	template_name="user/password_reset_complete.html"),name="password_reset_complete"),

	path('profile/',views.profile,name='profile'),

]




from BlogShare import settings
from django.conf.urls.static import static
if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
