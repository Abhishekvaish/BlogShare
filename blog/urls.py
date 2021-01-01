from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
	path('home/',views.Home.as_view(),name='home'),

	path('<int:pk>/<str:title>/',views.detail,name='detail'),

	path('user/<int:pk>/',views.user_post,name="user_post"),

	path('new_post/',views.NewPost.as_view(),name='new_post'),

	path('<int:pk>/<str:title>?edit=true',views.UpdatePost.as_view(),name='update'),

]