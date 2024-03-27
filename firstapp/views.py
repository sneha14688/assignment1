from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib import messages
import requests
from django.contrib.auth.decorators import login_required
from .forms import BlogForm
from .models import Blogger, Blog
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import BlogSerializer
from .permissions import IsSiteAdmin
from rest_framework import status 
from .forms import BlogForm
import time


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, f'Welcome, {user.username}!')
            return redirect('home')  # replace 'home' with your desired URL after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')  # create a login.html template in your app's templates folder



def user_logout(request):
    logout(request)
    # messages.info(request, 'You have been logged out.')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')  # assuming you have a login URL named 'login'
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})



# @login_required
def home(request):
    #requests.urllib3.disable_warnings()
    
    api_key = 'fcab833e9d1d4812a379ad9a32294015'
    url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
    page = ''
    while page == '':
        try:
            response = requests.get(url, verify=False, timeout=30)
            news_data = response.json()['articles']
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue

    return render(request, 'home.html', {'news_data': news_data})





def blogList(request):
    blogs = Blogger.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

@login_required
def delete_blog(request, blog_id):
    print(request, blog_id)
    blog = get_object_or_404(Blog, id=blog_id)

    if request.method == 'POST':
        blog.delete()
        # messages.success(request, 'Blog post deleted successfully.')
        return redirect('delete_success')  # Redirect to your desired page after deletion

    return render(request, 'delete_blog.html', {'blog_id': blog.id})





def create_blog(request):
    print(request.POST)
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = request.user  # Assuming the user is logged in
            blog = Blog.objects.create(title=title, content=content, author=author)
            return redirect('blog_details')  # Redirect to blog detail page
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})


def blog_details(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_details.html', {'blogs': blogs})



def index(request):
    return render(request, 'index.html', {})

def delete_success(request):
    return render(request, 'delete_success.html',{})


#Serializers - Django REST Framework
@api_view(['GET'])
@permission_classes([IsSiteAdmin])
def blog_list_api(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsSiteAdmin])
def create_blog_api(request):
    print(request.data)
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = request.user  # Assuming the user is logged in
            blog = Blog.objects.create(title=title, content=content, author=author)
            return redirect('blog_details')  # Redirect to blog detail page
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})



@api_view(['DELETE'])
@permission_classes([IsSiteAdmin])
def delete_blog_api(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        return Response({"message": "Blog not found"}, status=status.HTTP_404_NOT_FOUND)
    
    blog.delete()
    return Response({"message": "Blog deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_blog_api(request, pk):
    try:
        blog_post = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(blog_post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def endpoints(request):
    return render(request, 'rest_endpoints.html',{})