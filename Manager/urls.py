from django.urls import path
from . import views

urlpatterns = [
	path('',views.index, name='index'),
    path('signup/', views.signup, name='signup'),    
    path('logout/', views.logout, name='logout'),
    path('update1/', views.update_one, name='update_one'),
    path('update2/', views.update_two, name='update_two'),
    path('update3/', views.update_three, name='update_three'),
    path('download/', views.download, name='download'),
    path('glory/', views.glory, name='glory'),
    path('blog/', views.blog, name='blog'),
]
