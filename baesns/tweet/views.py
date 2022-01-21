from contextlib import redirect_stderr
import imp
import re
from winreg import REG_QWORD
from django.shortcuts import render,redirect
from .models import TweetComment, TweetModel
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, TemplateView

# Create your views here.
def home(request):
    user = request.user.is_authenticated

    if user:
        return redirect('/tweet')
    else:
        return redirect('/sign-in')

def tweet(request):
    
    if request.method =="GET":
        user = request.user.is_authenticated
        if user:
            all_tweet = TweetModel.objects.all().order_by('-created_date')
            return render(request,'tweet/home.html',{'tweet':all_tweet})
        else:
            return redirect('/sign-in')
    elif request.method =="POST":
        content = request.POST.get('my-content','')

        
        if content == '':
            all_tweet = TweetModel.objects.all().order_by('-created_date')
            return render(request,'tweet/home.html',{'error':'글은 필수요소입니다.','tweet':all_tweet})
            
        
        
        else :
            user = request.user
            tags = request.POST.get('tag','').split(',')
            my_tweet = TweetModel.objects.create(author=user, content=content)
            for tag in tags:
                tag = tag.strip()
                if tag != '':
                    my_tweet.tags.add(tag)

            my_tweet.save()
            return redirect('/tweet')

@login_required
def delete_tweet(request,id):
        my_tweet = TweetModel.objects.get(id=id)
        my_tweet.delete()
        return redirect('/tweet')

@login_required
def detail_tweet(request,id):
        show_detail = TweetModel.objects.get(id=id)
        tweet_comment = TweetComment.objects.filter(tweet_id=id).order_by('-created_at')
        return render(request,'tweet/tweet_detail.html',{'tweet':show_detail,'comment':tweet_comment})

@login_required
def write_comment(request,id):
    if request.method == "POST":
        tweet_id = TweetModel.objects.get(id=id)
        comment = request.POST.get('comment','')

        my_comment = TweetComment()
        my_comment.tweet = tweet_id
        my_comment.author = request.user
        my_comment.comment = comment
        my_comment.save()

        return redirect('/tweet/'+str(id))

@login_required
def delete_comment(request,id):
        comment = TweetComment.objects.get(id=id)
        a = comment.tweet.id
        print(a)
        comment.delete()

        return redirect('/tweet/'+ str(a))


class TagCloudTV(TemplateView):
    template_name = 'taggit/tag_cloud_view.html'


class TaggedObjectLV(ListView):
    template_name = 'taggit/tag_with_post.html'
    model = TweetModel

    def get_queryset(self):
        return TweetModel.objects.filter(tags__name=self.kwargs.get('tag'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tagname'] = self.kwargs['tag']
        return context
