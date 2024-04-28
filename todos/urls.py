from django.urls import path
from .views import *
from endpoints.users import *
from . import views

urlpatterns = [
    # path('create', views.registertodo),
    # path('app/<int:pk>', views.Updatingtodos.as_view()),
    # path('app', views.Creatingandgetting.as_view()),
    path('create', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view())
    # path('retrive/<int:pk>', views.retrive)
    # path('<int:pk>/', DetailTodo.as_view()),
    # path('', ListTodo.as_view()),
    # path('create', CreateTodo.as_view())
    # path('delete/<int:pk>', DeleteTodo.as_view())
]