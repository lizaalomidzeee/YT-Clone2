from multiprocessing import context
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from .models import video, Comment, Category
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class Index(ListView):
    model = video
    template_name = 'videos/index.html'
    order_by = '-date_posted'

class CreateVideo(LoginRequiredMixin, CreateView):
    model = video
    fields = ['title', 'description', 'video_file', 'thumbnail', 'category']
    template_name = 'videos/create_video.html'
 

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)
        
    
 

    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.pk})



class DetailVideo(View):
    def get(self, request, pk, *args, **kwargs):
        
        video_obj = get_object_or_404(video, pk=pk)  
        
        
        form = CommentForm()
        comments = Comment.objects.filter(video=video_obj).order_by('-created_on')
        
        
        categories = video.objects.filter(category=video_obj.category)[:15]  
        
        context = {
            'objects': video_obj,
            'comments': comments,
            'categories': categories,  
            'form': form
        }
        return render(request, 'videos/detail_video.html', context)
    
    def post(self, request, pk, *args, **kwargs):
        
        video_obj = get_object_or_404(video, pk=pk)  
        
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = Comment(
                user=self.request.user,
                comment=form.cleaned_data['comment'],
                video=video_obj
            )
            comment.save()
        
        
        comments = Comment.objects.filter(video=video_obj).order_by('-created_on')
        
        
        categories = video.objects.filter(category=video_obj.category)[:15]  
        
        context = {
            'objects': video_obj,
            'comments': comments,
            'categories': categories,
            'form': form
        }
        return render(request, 'videos/detail_video.html', context)
    
    
    
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'videos/category_detail.html'  
    context_object_name = 'category'  
        
    

class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = video
    fields = ['title', 'description']
    template_name = 'videos/create_video.html'

    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader

class DeleteVideo(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = video
    template_name = 'videos/delete_video.html'

    def get_success_url(self):
        return reverse('index')
    
    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader
    
    

class VideoCategoryList(View):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        videos = video.objects.filter(category=category).order_by('-date_posted')
        
        
        context = {
            'category': category,
            'videos': videos
        }
        
        return render(request, 'videos/video_category.html', context)