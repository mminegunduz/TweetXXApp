
from django.urls import path
from . import views

app_name= 'tweetapp'


urlpatterns = [
    path('',views.listtweet,name='listtweet'), #//
    path('addtweet',views.addtweet,name='addtweet'),  #//addtweet
    path('addtweetbyform', views.addtweetbyform, name='addtweetbyform'), 
    path('addtweetbymodelform', views.addtweetbymodelform, name='addtweetbymodelform'),
    path('signup/', views.SignUpView.as_view(),name="signup"), #//signup
    path("deletetweet/<int:id>", views.deletetweet, name="deletetweet")  # //deletetweet  urllerini yazarak direkt o sayfaya ulaşılabilir.
   ]


