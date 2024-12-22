from django.contrib import admin
from  tweetapp.models import Tweet
#from . import Models

# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    fieldsets=[
        ('Message Group', {"fields": ["message"]}),
        ('Nickname Group', {"fields": ["nickname"]})
    ]

    #fields = ['nickname','message']



admin.site.register(Tweet,TweetAdmin)
