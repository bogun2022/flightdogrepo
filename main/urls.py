from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name = 'index'), #From tutorial!!!
#    path('main/home', views.home, name = 'home'),  #From tutorial!!!
    path('index/', views.index, name = 'index'),
    path('main/<int:state_id>/', views.details, name = 'details'),
    path('sign-up', views.sign_up, name = 'sign_up'),  #From tutorial!!!
]

print(path('<int:state_id>/', views.details, name = 'details'))
