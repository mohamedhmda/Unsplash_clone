from logging import error
from django.conf.urls import url
from django.http.response import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls.base import reverse_lazy
from django.views import generic
from django.urls import reverse
from django.views.generic.detail import DetailView
import requests
import base64
from notifications.signals import notify

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views.generic.edit import  UpdateView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Collection, Follower, Image,Like
from .forms import SignupForm,UploadImageForm
from .mixins import OwnerRequiredMixin, UserEditMixin

import wget, os

from taggit import utils as taggit_utils

from pathlib import Path




BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.


class HomeView(generic.ListView):
    template_name = 'api/index.html'
    context_object_name = 'Images'

    def get_queryset(self):
        return Image.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs) # get the default context data
        if self.request.user.is_authenticated:
            context['liked'] = Like.objects.filter(user=self.request.user).values_list("image", flat=True)
            context['collections'] = list(Collection.objects.filter(user=self.request.user))
        context['intro_pic'] = Image.objects.last()
        return context
##
## working with images
##
class ImageDetailView(DetailView):
    model = Image
    template_name = 'api/image_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ImageDetailView, self).get_context_data(**kwargs) # get the default context data
        if self.request.user.is_authenticated:
            context['liked'] = Like.objects.filter(user=self.request.user,image=self.object)
            context['collections'] = list(Collection.objects.filter(user=self.request.user))
            context['in_collections'] = self.object.collection_set.all()
        return context

@login_required
def UploadImage(request):
    template_name = 'api/image_upload_form.html'
    # if this is a POST request         
    if request.method == 'POST':
        form = UploadImageForm(request.POST,request.FILES)
        if form.is_valid():
            response = handle_uploaded_file(request.FILES['photo'])
            obj = form.save(commit=False)
            obj.user = request.user
            obj.photo = response.json()['data']['image']['url']
            obj.delete_url = response.json()['data']['delete_url']
            
            obj.save()
            form.save_m2m()
            return redirect(reverse('api:profile',kwargs={'pk':request.user.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadImageForm()
        
    return render(request, template_name, {'form': form})

##############################################
def handle_uploaded_file(file):
    
    API_imgbb = "6cd34de2e4bc11577e8d978a4be5ba06"
    url = "https://api.imgbb.com/1/upload"

    payload = {
        "key": API_imgbb,
        "image": base64.b64encode(file.read()),
    }
    res = requests.post(url, payload)
    
    return res
##############################################

@method_decorator(login_required, name='dispatch')
class EditImage(OwnerRequiredMixin, UpdateView):
    model = Image
    fields = ('tags', 'description', 'location')

    def get_success_url(self):
        return reverse_lazy('api:image',kwargs={'pk':self.kwargs['pk']})

    # ~~~~~~~~~~~ to be reviewed ( choose one )

@method_decorator(login_required, name='dispatch')
class DeleteImagee(OwnerRequiredMixin, DeleteView):
    model = Image

    def get_success_url(self):
        return reverse_lazy('api:profile',kwargs={'pk':self.request.user.id})

@login_required
def DeleteImage(request, image_id):
    image = get_object_or_404(Image, pk=image_id, user=request.user)
    image.delete()
    return redirect(reverse('api:profile',kwargs={'pk':request.user.id}))
    # ~~~~~~~~~~~ 


def DownloadImage(request,image_id):
    image = get_object_or_404(Image, pk=image_id)
    image_path = os.path.join(BASE_DIR, "images")

    image_filepath = wget.download(image.photo, out = image_path)
    image_filename = os.path.basename(image_filepath)

    data = {
        'image_filename' : image_filename
    }
    return JsonResponse(data)


def DeleteImageFromLocal(request,image_name):
    image_path = os.path.join(BASE_DIR, "images")
    image_file = image_path+"/"+image_name
    if os.path.exists(image_file):
        os.remove(image_file)
    
    return JsonResponse({})

@login_required
def like_image(request,image_id):
    user = get_object_or_404(User, pk=request.user.id)
    image = get_object_or_404(Image, pk=image_id)

    if Like.objects.filter(image_id=image.id, user_id=user.id).exists():
        return HttpResponse(status=404)
    else:
        like = Like(
            user = user,
            image = image
            )
        like.save()
        setattr(image, "likes", getattr(image,"likes")+1)
        image.save()
        notify.send(
                    request.user,
                    recipient = image.user,
                    verb = "Liked your image",
                    target = image
                    )
    return redirect(reverse('api:home'))

@login_required
def unlike_image(request,image_id):
    like = get_object_or_404(Like, image_id=image_id, user_id=request.user.id)
    setattr(like.image, "likes", getattr(like.image,"likes")-1)
    like.image.save()
    like.delete()
    return redirect(reverse('api:home'))


##
## search
##

class SearchView(generic.ListView):
    template_name = 'api/search.html'
    context_object_name = 'Images'

    def get_queryset(self):
        taglist = taggit_utils.parse_tags(self.request.GET.get('tags'))
        return Image.objects.filter(
            tags__name__in=taglist
        ).distinct()

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs) # get the default context data
        context['tags'] = taggit_utils.parse_tags(self.request.GET.get('tags'))
        return context

##
## working with collections
##

class CollectionDetailView(DetailView):
    model = Collection

@method_decorator(login_required, name='dispatch')
class CreateCollection(CreateView):
    model = Collection
    fields = ('name','description','private')
    success_url = reverse_lazy('api:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateCollection, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('api:collection',kwargs={'pk':self.kwargs['pk']})

@method_decorator(login_required, name='dispatch')
class EditCollection(OwnerRequiredMixin, UpdateView):
    model = Collection
    fields = ('name','description','private')
    def get_success_url(self):
        return reverse_lazy('api:collection',kwargs={'pk':self.kwargs['pk']})

@method_decorator(login_required, name='dispatch')
class DeleteCollection(OwnerRequiredMixin, DeleteView):
    model = Collection

    def get_success_url(self):
        return reverse_lazy('api:profile',kwargs={'pk':self.request.user.id})

@login_required
def AddImageToCollection(request, collection_id, image_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    image = get_object_or_404(Image, pk=image_id)

    if collection.user == request.user:
        if not collection.images.filter(pk=image.id).exists():
            collection.images.add(image)
            
    return redirect(reverse('api:image',kwargs={'pk':image.id}))

@login_required
def RemoveImageFromCollection(request,collection_id, image_id):
    collection = get_object_or_404(Collection, pk=collection_id)
    image = get_object_or_404(Image, pk=image_id)

    if collection.user == request.user:
        if collection.images.filter(pk=image.id).exists():
            collection.images.remove(image) 

    return redirect(reverse('api:image',kwargs={'pk':image.id}))



##
## profile
##

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            new_follower = Follower.objects.create(user = user)
            return redirect(reverse('api:home'))
    else:
        form = SignupForm()
    return render(request, 'account/signup.html', {'form': form})

class ProfileDetailView(DetailView):
    model = User
    template_name = 'api/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs) # get the default context data
        context['i_follow'] = list(self.object.followers.all())
        x = self.object.follower_set.first()
        context['followers'] = list(x.followers.all()) if x is not None else []
        context['liked'] = Like.objects.filter(user=self.request.user).values_list("image", flat=True)
        return context


@method_decorator(login_required, name='dispatch')
class EditProfileView(UserEditMixin, UpdateView):
    model = User
    template_name = 'registration/edit.html'
    fields = ('username','first_name','last_name','email')
    success_url = reverse_lazy('api:home')

@login_required
def FollowUser(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    user_followed, created = Follower.objects.get_or_create(
        user = user
    )
    follower = request.user
    if user != follower:
        if user_followed.followers.filter(pk=follower.id).exists():
            return HttpResponse("already follower")
        else:
            user_followed.followers.add(follower)
            notify.send(
                follower,
                recipient = user,
                verb = "Started following you"
                )
            return redirect(reverse('api:profile',kwargs={'pk':user.id}))
    else:
        return HttpResponse("cant follow yourself")

@login_required
def UnfollowUser(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    user_followed = get_object_or_404(Follower, user=user)
    follower = request.user
    if user != follower:
        if user_followed.followers.filter(pk=follower.id).exists():
            user_followed.followers.remove(follower)
            return redirect(reverse('api:profile',kwargs={'pk':user.id}))
        else:
            return HttpResponse("you are not a follower")
    else:
        return HttpResponse("cant unfollow yourself")

@login_required
def notifications_view(request):
    return render(request, 'api/notifications.html')