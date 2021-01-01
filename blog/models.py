from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.urls import reverse

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = RichTextField(blank=False,null=False)
	# content = models.TextField()
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now=True)
	tags = models.CharField(max_length=255)
	likes = models.ManyToManyField("Like")

	def get_absolute_url (self):
		return reverse('blog:detail',kwargs={"pk":self.pk,"title":self.title})

	def __str__(self):
		return self.title

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
	text = models.TextField()
	time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.text

class Like(models.Model):
	user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

	def __str__(self):
		return self.user.email