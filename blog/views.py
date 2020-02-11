from django.shortcuts import render
from django.http import HttpResponse
from .models import Post 
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


posts=[
  {
	'author':'CoreyMS',
	'title':'Blog-Post 1',
	'content':'First blog post content 1',
	'date_posted':'August 27, 2018'
  },
  {
	'author':'Jane Doe',
	'title':'Blog-Post 2',
	'content':'Second blog post content 2',
	'date_posted':'july 16, 2019'
  }
]

def home(request):
	#return HttpResponse('<h1>Blog-Home</h1>')
	context={
	'posts':Post.objects.all()
	}
	return render(request,'blog/home.html',context)

def about(request):
	#return HttpResponse('<h1>Blog-About</h1>')
	return render (request,'blog/about.html',{'title':'About'})

class PostListView(ListView):
	model=Post
	template_name='blog/home.html'
	context_object_name='posts'
	ordering=['-date_posted']

class PostDetailView(DetailView):
	model=Post

#class PostCreateView(CreateView):
class PostCreateView(LoginRequiredMixin, CreateView):
	model=Post
	fields=['title','content']
	def form_valid(self, form):
		form.instance.author=self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UpdateView):
	model=Post
	fields=['title','content']
	def form_valid(self,form):
		form.instance.author=self.request.user
		return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model=Post
	success_url='/'
	def test_func(self):
		post=self.get_object()
		if self.request.user==post.author:
			return True
		return False	

