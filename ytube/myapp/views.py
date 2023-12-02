from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from django.contrib import auth
from django.contrib.auth.models import User , auth 
from django.contrib.auth import logout
from .models import ChannelsForm , ChannelVideo , Subscription , Comment ,Cart ,Shorts , CommunitymPost

from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import ChannelDetailsForm , VideoDetailsForm , ChannelShorts , ChannelCommunity
# Create your views here.

def signuplogin(request):
    if request.method == 'POST':
        
        if 'email' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            data = User.objects.create_user(username=username,email=email,password=password1)
            data.save()
            return redirect('signuplogin')
        
        elif 'username' in request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('home')
        
            else:
                return redirect('signuplogin')
        
    # elif 'logout' in request.GET:
    #     auth.logout(request)
    #     return redirect('signuplogin')  # Redirect to the home page after logout

    return render(request, 'first/signuplogin.html')
            
def logout(request):
    auth.logout(request)
    return redirect('signuplogin')

def home(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)

    channeldata = ChannelsForm.objects.filter(user=request.user)
    data = ChannelVideo.objects.all()
    
    return render(request,'first/home.html',{'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url ,'data':data ,'channeldata':channeldata})

def channel(request):
    # if request.method == 'POST':
    #     form = ImageUploadedForm(request.POST , request.FILES)
    #     if form.is_valid():
    #         form.save()
    # form = ImageUploadedForm()
    user = request.user
    if request.method == 'POST':
        forms = ChannelDetailsForm(request.POST , request.FILES)
        
        if forms.is_valid():
            forms.instance.user = request.user
            forms.save()
        
        return redirect('home')
    forms = ChannelDetailsForm()
    data = ChannelsForm.objects.filter(user=request.user)
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    return render(request,'first/channel.html',{'data':data,'forms':forms,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url})


def userprofile(request):

    channelvideos = ChannelVideo.objects.all()
    data = ChannelsForm.objects.filter(user=request.user)

    # channel = ChannelsForm.objects.get(pk=channel_id)
    # channel.subscibers += 1
    # channel.save()

    print(data)
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    return render(request,'userchannel/userprofile.html',{'data':data,'channelvideos':channelvideos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url})

def usercommunity(request):
    channelvideos = ChannelVideo.objects.all()
    data = ChannelsForm.objects.filter(user=request.user)
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)

    if request.method == 'POST':
        comforms = ChannelCommunity(request.POST , request.FILES)
        
        if comforms.is_valid():
            comforms.instance.user = request.user
            comforms.save()
        
        return redirect('home')
    comforms = ChannelCommunity()

    return render(request,'userchannel/community.html',{'data':data,'channelvideos':channelvideos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url,'comforms':comforms })

def userupload(request):
   
    if request.method == 'POST':
        forms = VideoDetailsForm(request.POST , request.FILES)
        
        if forms.is_valid():
            forms.instance.user = request.user
            forms.save()
        
        return redirect('home')
    forms = VideoDetailsForm()
    channelvideos = ChannelVideo.objects.all()
    data = ChannelsForm.objects.filter(user=request.user)
    # data = ChannelVideo.objects.filter(user=request.user)
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    return render(request,'userchannel/useruploads.html',{'forms':forms,'data':data,'channelvideos':channelvideos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url})

def uploadshorts(request):
    if request.method == 'POST':
        shortforms = ChannelShorts(request.POST , request.FILES)
        
        if shortforms.is_valid():
            shortforms.instance.user = request.user
            shortforms.save()
        
        return redirect('home')
    shortforms = ChannelShorts()
    channelvideos = ChannelVideo.objects.all()
    data = ChannelsForm.objects.filter(user=request.user)
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    return render(request,'userchannel/shortsupload.html',{'shortforms':shortforms,'data':data,'channelvideos':channelvideos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url})


# def view_video(request, video_id):
#     video = get_object_or_404(ChannelVideo, id=video_id)
#     video.views += 1
#     video.save()

def videopage(request,post_slug):
    video = get_object_or_404(ChannelVideo, slug=post_slug)
    # calculating views 
    viewed_video_key = f'viewed_video_{video.id}'
    if not request.session.get(viewed_video_key, False):
        # Increment views only if the user hasn't viewed the video in this session
        video.views += 1
        video.save()

        # Set a session variable to indicate that the user has viewed the video
        request.session[viewed_video_key] = True
    # end of calculating views 

    post = get_object_or_404(ChannelVideo, slug=post_slug)
    videosdata = ChannelVideo.objects.all()
    if request.method == 'POST':
        content = request.POST.get('content')
        user = request.user  # Assuming you have user authentication

        if content:
            Comment.objects.create(video=post, user=user, content=content)

        # Check if the form submitted is the like button
        elif 'like_button' in request.POST:
            video.likes += 1
            video.save()
        # Check if the form submitted is the like button
        elif 'dislike_button' in request.POST:
            video.likes -= 1
            video.save()
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    comments = Comment.objects.filter(video=post).order_by('-created_at')
    context = {'post': post,'videosdata':videosdata,'video': video,'comments': comments,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url}
    return render(request,'videoplay/videopage.html',context)

# def like_video(request, video_id):
#     video = get_object_or_404(Video, id=video_id)
#     video.likes += 1
#     video.save()

    # return HttpResponse(f'Liked video: {video.title}! Likes: {video.likes}')

#Buillding nav options 
def subscribing(request):
    return render(request,'navoptions/subscriptions.html')

def addtomylist(request):
    user = request.user
    video_id = request.GET.get('post_id')
    video = ChannelVideo.objects.get(id=video_id)
    Cart(user=user ,movie=video).save()
    return redirect('/mylist')

def remove_mylist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('post_id')
        try:
            cart_item = Cart.objects.get(user=request.user, movie_id=prod_id)
            cart_item.delete()
            return redirect('/mylist')
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Item not found in your cart'}, status=404)

def mylist(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)

    user = request.user
    cart = Cart.objects.filter(user=user)
    print(cart)
    channelvideos = ChannelVideo.objects.all()
    return render(request,'navoptions/mylist.html',{'carts':cart,'channelvideos':channelvideos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

def most_likedvideos(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)

    
    most_like_videos = ChannelVideo.objects.all().order_by('-likes')[:30]
    context = {'most_like_videos':most_like_videos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url }
    return render(request,'navoptions/likedvideos.html',context)

def most_watched(request):
    most_watched_videos = ChannelVideo.objects.all().order_by('-views')[:30]


    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)

    return render(request,'navoptions/mostwatched.html',{'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url,'most_watched_videos':most_watched_videos })

def settings(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    return render(request,'navoptions/settings.html',{'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

# Filtering videos and displaying 
def action_videos(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    videos = ChannelVideo.objects.filter(category='X')
    return render(request, 'filters/action.html', {'videos': videos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

def anime_videos(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    videos = ChannelVideo.objects.filter(category='AN')
    return render(request, 'filters/anime.html', {'videos': videos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

def film_videos(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    videos = ChannelVideo.objects.filter(category='K')
    return render(request, 'filters/film.html', {'videos': videos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

def gaming_videos(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    videos = ChannelVideo.objects.filter(category='G')
    return render(request, 'filters/gaming.html', {'videos': videos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

def learning_videos(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    videos = ChannelVideo.objects.filter(category='L')
    
    return render(request, 'filters/learning.html', {'videos': videos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

def fashion_videos(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    videos = ChannelVideo.objects.filter(category='F')
    return render(request, 'filters/fashion.html', {'videos': videos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

def sports_videos(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    videos = ChannelVideo.objects.filter(category='S')
    return render(request, 'filters/sports.html', {'videos': videos,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })


def shorts(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    data = Shorts.objects.all()
    return render(request, 'videoplay/shorts.html',{'data':data,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

# def uploadshorts(request):
#     if request.method == 'POST':
#         shortforms = ChannelShorts(request.POST , request.FILES)
        
#         if shortforms.is_valid():
#             shortforms.instance.user = request.user
#             shortforms.save()
        
#         return redirect('home')
#     shortforms = ChannelShorts()

#     return render(request,'userchannel/shortsupload.html',{'shortforms':shortforms})

def searchpage(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)

    query = request.GET.get('q')  # Get the search query from the request
    results = ChannelVideo.objects.filter(videotitle__icontains=query) if query else None
    return render(request,'navoptions/search.html',{'results': results, 'query': query,'user_channel_data':user_channel_data , 'dynamic_url':dynamic_url })

def communitypost(request):
    user_channel_data = ChannelsForm.objects.filter(user=request.user).exists()
    if user_channel_data:
        url_name = 'userprofile'
    else:
        url_name = 'channel'
    dynamic_url = reverse(url_name)
    data = CommunitymPost.objects.all()
    context = {'data':data,'dynamic_url':dynamic_url}
    return render(request,'videoplay/communitypost.html',context)