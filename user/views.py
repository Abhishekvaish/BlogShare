from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from .forms import UserRegistrationForm,UserUpdateForm

from django.contrib import messages # can send msg to view when redirecting 

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from background_task import background


def index(request):
	return render(request, template_name='user/index.html')

@background(schedule=60*10)
def check_user(user_id):
	user = get_user_model().objects.get(pk=user_id)
	if not user.is_active:
		user.delete()


def register(request):
	context = { 'form':UserRegistrationForm }

	if request.method == "POST":
		form = UserRegistrationForm(request.POST)
		context['form'] = form
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			check_user(user.pk)
			mail_subject = 'Activate your BlogShare account.'

			message = render_to_string('user/activate_account.html', {
			'user': user,
			'domain': get_current_site(request).domain,
			'uid':urlsafe_base64_encode(force_bytes(user.pk)),
			'token':account_activation_token.make_token(user),
			})
			email = EmailMessage(
			mail_subject, message, to=[user.email]
			)
			email.content_subtype = 'html'
			email.send()

			
			context = {
				"confirmation":True,
				"email":user.email
			}
			return render(request, template_name='user/msg.html',context=context)

	return render(request, template_name='user/register.html',context=context)


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = get_user_model().objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		#messages.success(request, "Your Account has been verified successfully you can go ahead and signIn")
		login(request, user)
		return redirect('blog:home')
	else:
		return render(request, 'user/msg.html',{'invalid':True})

@login_required
def profile(request):
	if request.method == "GET":
		context  = {'form':UserUpdateForm(instance=request.user)}
		return render(request, template_name='user/profile.html',context=context)
	elif request.method == "POST":
		form = UserUpdateForm(request.POST,request.FILES,instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('profile')
		else:
			context  = {'form':form}
			return render(request, template_name='user/profile.html',context=context)

