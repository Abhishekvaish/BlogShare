from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,CreateView,UpdateView
from .models import Post,Comment,Like
from django.template.defaultfilters import register
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http  import JsonResponse
from django.forms.models import model_to_dict



@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.strip().split(key)
@register.filter(name="url_format")
def url_format(title):
	return title.strip().replace(' ','-')

class Home(ListView):
	model = Post
	template_name = 'blog/home.html' #default_name = 'blog/post_list.html'
	context_object_name = 'post_list' #default_name = 'object_list'
	ordering = '-created_on'
	paginate_by = 20




def detail(request,pk,title):
	if request.is_ajax() and request.GET.get("like"):
		if not request.user:return JsonResponse({},status=404)
		post = get_object_or_404(Post,pk=pk)

		if request.GET.get("like") == "false":
			post.likes.filter(user=request.user).delete()
			post.save()
			print("like - 1 ")
		elif request.GET.get("like") == "true":
			if not post.likes.filter(user=request.user):
				post.likes.create(user=request.user)
				post.save()
			print("like + 1 ")
		return JsonResponse({},status=200)

	elif request.is_ajax() and request.GET.get("comment"):
		if not request.user:return JsonResponse({},status=404)
		post = get_object_or_404(Post,pk=pk)
		if request.method == "POST":
			text = request.POST["text"].strip()
			post.comment_set.create(author = request.user,text=text)
			post.save()

			data = {'comments' : [
			{
				"pk":c.pk,
				"author_same_as_user":True if request.user.is_authenticated and request.user.pk==c.author.pk else False ,
				"author_pk":c.author.pk,
				"author_img" : c.author.img.url,
				"text":c.text,
				"author_name": (c.author.first_name + " "+c.author.last_name).lower(),
				"time": c.time
			} for c in post.comment_set.all()] }
			return JsonResponse(data=data,status=200)

	elif request.is_ajax() and request.GET.get("delete_comment"):
		if not request.user:return JsonResponse({},status=404)
		post = get_object_or_404(Post,pk=pk)
		if request.method == "POST":
			Comment.objects.filter(pk=request.POST["pk"]).delete()
			data = {'comments' : [
			{
				"pk":c.pk,
				"author_same_as_user":True if request.user.is_authenticated and request.user.pk==c.author.pk else False ,
				"author_pk":c.author.pk,
				"author_img" : c.author.img.url,
				"text":c.text,
				"author_name": (c.author.first_name + " "+c.author.last_name).lower(),
				"time": c.time
			} for c in post.comment_set.all()] }
			return JsonResponse(data=data,status=200)

	elif request.is_ajax():
		post = get_object_or_404(Post,pk=pk)
		comments = post.comment_set.all()
		if request.user.is_authenticated:
			try:
				post.likes.get(user=request.user)
				data = {'liked':True}
			except :
				data = {'liked':False}
		data = {'comments' : [
		{
			"pk":c.pk,
			"author_same_as_user":True if request.user.is_authenticated and request.user.pk==c.author.pk else False ,
			"author_pk":c.author.pk,
			"author_img" : c.author.img.url,
			"text":c.text,
			"author_name": (c.author.first_name + " "+c.author.last_name).lower(),
			"time": c.time
		} for c in comments ]}
		data['like_count'] = len(post.likes.all())
		return JsonResponse(data=data,status=200)
	else:
		post = get_object_or_404(Post,pk=pk)
		context = {'post':post}
		return render(request, template_name='blog/post_detail.html',context=context)


def user_post(request,pk):

	if request.method == "POST":
		print(request.POST)
		Post.objects.filter(pk=int(request.POST["pk"])).delete()
	user = get_object_or_404(get_user_model(),pk=pk)
	context  = {
		'posts':Post.objects.filter(author=user),
		'owner':False,
		'author':user
	}
	if request.user.is_authenticated and request.user == user :
		context['owner']=True
	return render(request, template_name='blog/user_post.html',context=context)


class NewPost(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title','content','tags']
	template_name = 'blog/post_create.html'  # default = 'blog/post_form.html'
	context_object_name = 'form' # default = form 

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class UpdatePost(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	fields = ['title','content','tags']
	template_name = 'blog/post_create.html'  # default = 'blog/post_form.html'
	context_object_name = 'form' # default = form 

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else :
			return False

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)


