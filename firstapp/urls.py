from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    
    path('home/', views.home, name = "home"),
    # path('createBlog/', views.createBlog, name ="createBlog"),
    path('blogList', views.blogList, name='blogList'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
    path('create_blog/', views.create_blog, name="create_blog"),
    path('blog_details/',views.blog_details,name='blog_details'),
    path('delete_blog/', views.delete_blog, name='delete_blog'),
    path('delete_success/', views.delete_success, name='delete_success'),

    #API enpoints only accessible to system admin
    path('endpoints/', views.endpoints, name="endpoints"),
    path('blog_list_api/', views.blog_list_api, name='blog_list_api'),
    path('create_blog_api/', views.create_blog_api, name="create_blog_api"),
    path('delete_blog_api/<int:id>', views.delete_blog_api, name="delete_blog_api"),
    path('update_blog_api/<int:id>', views.update_blog_api, name="update_blog_api"),
]
