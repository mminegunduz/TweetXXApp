import threading
from django.shortcuts import render, redirect
from . import models
from django.urls import reverse, reverse_lazy
from tweetapp.forms import AddTweetForm, AddTweetModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
import threading
import logging


#gönderileri listeleyen fonksiyon kodu
def listtweet(request):
    all_tweets = models.Tweet.objects.all().order_by('-id')  #atılan son gönderiyi başa alıp listeleyen method.
    tweet_dict = {"tweets": all_tweets}
    return render(request, 'tweetapp/listtweet.html', context=tweet_dict)


#kullanıcı giriş yapıtığında olacak olayların fonksiyon kodları
@login_required(login_url="/login")
# kullanıcı girdiğinde gönderi ekle sayfasına gönderisini yazıp ekleyen fonksiyon kodları
def addtweet(request):
    if request.POST:
        message = request.POST["message"]

        # Threading ile tivit yükleme işlemini arka planda yapalım
        thread = threading.Thread(target=create_tweet, args=(request.user, message))
        thread.start()    #thread kullanarak eş zamanlı gönderi atımı gerçekleştirildi.

        return redirect(reverse('tweetapp:listtweet'))
    else:
        return render(request, 'tweetapp/addtweet.html')

def create_tweet(user, message):
    # Thread içinde yapılacak işlem
    models.Tweet.objects.create(username=user, message=message)


# gönderi eklemek için yazılan 
def addtweetbyform(request):
    if request.method == "POST":
        form = AddTweetForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data["nickname_input"]
            message = form.cleaned_data["message_input"]
            models.Tweet.objects.create(nickname=nickname, message=message)
            return redirect(reverse('tweetapp:listtweet'))
        else:
            print("error in form!")
            return render(request, 'tweetapp/addtweetbyform.html', context={"form": form})
    else:
        form = AddTweetForm()
        return render(request, 'tweetapp/addtweetbyform.html', context={"form": form})

def addtweetbymodelform(request):
    if request.method == "POST":
        form = AddTweetModelForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data["nickname"]
            message = form.cleaned_data["message"]
            models.Tweet.objects.create(nickname=nickname, message=message)
            return redirect(reverse('tweetapp:listtweet'))
        else:
            print("error in form!")
            return render(request, 'tweetapp/addtweetbymodelform.html', context={"form": form})
    else:
        form = AddTweetModelForm()
        return render(request, 'tweetapp/addtweetbymodelform.html', context={"form": form})

@login_required

# silmek için yazılan fonksiyon
def deletetweet(request, id):
    tweet = models.Tweet.objects.get(pk=id)
    if request.user == tweet.username:
        models.Tweet.objects.filter(id=id).delete()
        return redirect('tweetapp:listtweet')


# kaydol sayfası için django tarafından otomatik oluşturması için yazılan kod.
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"




# threadin çalıştığını terminale göstermek amacıyla loglama konfigürasyonu yapıldı.
logging.basicConfig(level=logging.DEBUG)

def create_tweet(user, message):
    # Loglama ile işlem takip edildi. 
    logging.debug(f"Thread started for user: {user}, message: {message}")
    models.Tweet.objects.create(username=user, message=message)
    logging.debug(f"Thread finished for user: {user}, message: {message}")

@login_required(login_url="/login")
def addtweet(request):
    if request.POST:
        message = request.POST["message"]

        # Thread başlatılıyor
        thread = threading.Thread(target=create_tweet, args=(request.user, message))
        thread.start()

        # Başlatıldıktan sonra hemen dönüş yapıldı.
        logging.debug("Thread started for tweet creation.")
        return redirect(reverse('tweetapp:listtweet'))
    else:
        return render(request, 'tweetapp/addtweet.html')