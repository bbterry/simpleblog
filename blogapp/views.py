from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from simpleblog.settings import MEDIA_ROOT
from blogapp.models import Post, Img, User
from django.core.files.storage import FileSystemStorage
from PIL import Image
from forms import UploadImgForm
import datetime
import os.path

# Create your views here.

#Only people not logged in can only see public posts
def index(request):
	Posts = []
	status = ''
	username = ''
	level = 0
	if 'user' in request.session:
		status = 'logout'
		username = request.session['user']
		level = request.session['security_level']
		for post in Post.objects:
			Posts.append(post)
	else:
		status = 'login'
		for post in Post.objects:
			if post.viewable == 'P':
				Posts.append(post)
	return render_to_response('index.html', {'Posts': Posts, 'status' : status,
	'username': username, 'SecurityLevel': level}, RequestContext(request))

def register(request):
	if request.method == 'GET':
		return render_to_response('register.html',RequestContext(request))
	elif request.method == 'POST':
		d = request.POST
		pword = d['password']
		pword_repeat = d['password_repeat']
		
		if pword == pword_repeat:
			uname = d['username']
			for user in User.objects:
				if uname == user.username:
					return redirect(request, 'This user has existed', 'register')
			newuser = User(username=uname, password=pword)
			newuser.save()
			return redirect(request, 'Your account is registered successfully', 'login')
		else:
			return redirect(request, 'The passwords are not the same', 'register')
			
def login(request):
	if request.method == 'GET':
		if 'user' in request.session:
			return redirect(request, 'You have already logged in', '')
		else:
			return render_to_response('login.html', RequestContext(request))
	elif request.method == 'POST':
		d = request.POST
		uname = d['username']
		pword = d['password']
		
		for user in User.objects:
			if uname == user.username:
				if pword != user.password:
					return redirect(request, 'Username or password is invalid', 'login')
				else:
					if user.is_verify:
						request.session['user'] = user.username
						request.session['security_level'] = user.security_level
						if user.security_level == 10:
							return redirect(request, 'Welcome, administrator!', 'admin')
						return redirect(request, 'Login Successfully', '')
					else:
						return redirect(request, 'Your account is awaiting approval', '')				
			
		return redirect(request, 'Username or password is invalid', 'login')

def logout(request):
	if 'user' in request.session:
		del request.session['user']
		return redirect(request, 'You have successfully logged out', '')
	return redirect(request, 'You have not logged in', '')

#Only goduser can get access to this page	
def admin(request):
	if request.method == 'GET':
		if 'user' in request.session:
			if request.session['security_level'] == 10:
				Users = []
				for user in User.objects(is_verify=False):
					Users.append(user)
				return render_to_response('admin.html', {'Users': Users} ,RequestContext(request))
		return redirect(request, 'You are not admin', '')
	elif request.method == 'POST':
		d = request.POST
		uname = d['username']
		User.objects(username=uname).update(set__is_verify=True)
		return redirect(request, '', 'admin', 0)

#All variables should be filled(including upload image), a user must log in to make a post.
def add_post(request):
	if request.method == 'GET':
		if 'user' in request.session:
			return render_to_response('add_post.html', RequestContext(request))
		else:
			return redirect(request, 'You need to login to make a post', '')
	elif request.method == 'POST':
		d = request.POST
		title = d['title']
		content = d['content']
		date = datetime.datetime.now()
		viewable = d['viewable']
		author = None
		for user in User.objects(username=request.session['user']):
			author = user
		form = UploadImgForm(request.POST, request.FILES)
		if form.is_valid():
			newImg = Img(img_width = 50, img_height=50)
			newImg.img_src.put(request.FILES['img'], content_type = 'image/jpeg')
			newImg.save()			
			newPost = Post(title=title, content=content, date_added=date, image_id=newImg, author=author, viewable=viewable)
			newPost.save()
			return redirect(request, 'Added post successfully', '')
		return redirect(request, 'All inputs need to be filled', 'add_post')
		
		
#Only author or goduser can delete posts
def delete(request):
	if request.method == 'GET':
		if 'user' in request.session:
			d = request.GET
			id = d['id']
			username = d['username']
			return render_to_response('delete.html', {'id': id, 'username': username}, RequestContext(request))
		return redirect(request, 'Illegal operation!', '')				
	elif request.method == 'POST':
		if 'user' in request.session:
			d = request.POST
			if request.session['user'] == d['username'] or request.session['security_level'] == 10:
				id = d['id']
				if Post.objects(id=id).first().image_id is not None:
					img_id = Post.objects(id=id).first().image_id.id
					Img.objects(id=img_id).delete()
				Post.objects(id=id).delete()
				return redirect(request, 'deleted post successfully', '')
			
	return redirect(request, 'Illegal operation!', '')

def img_api(request,img_id):
	img = Img.objects(id=img_id).first()
	pic = img.img_src.read()
	content_type = img.img_src.content_type
	return HttpResponse(pic, content_type)
	
def redirect(request, title, path=None, delay=2000):
    if path is None:
        path = request.get_full_path()[1:]
    return render_to_response('redirect.html', {
        'host': request.get_host(),
        'title': title,
        'redirect': path,
        'delay': delay,
    })

#This function is to make inserting data more conveniently only for testing 
def database_operation(request):
	if 'user' in request.session:
		if request.session['security_level'] == 10:
			post1 = Post(title='Public article 2', content='test1', viewable='P').save()
			#post2 = Post(title='Private1', content='1eggrgwgwrhwrh', viewable='N').save()
			#post3 = Post(title='Private2', content='5635653768779', viewable='N').save()
			return redirect(request, 'Data inserted successfully', '')
	return redirect(request, 'Illegal operation!', '')
	
	
