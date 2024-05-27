from django.urls import path,include
from . import views
urlpatterns = [
    
    path('',views.index,name='index'),
    path('urlprocess',views.urlprocess,name='urlprocess'),
    path('process/', views.running_app_view, name='process'),

]