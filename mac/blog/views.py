from django.shortcuts import render
from django.http import HttpResponse
from . models import BlogPost

# Create your views here.
def index(request):
    blogs=BlogPost.objects.all()
    # for i in blogs:
        # print(i.post_id)
    #     print(i.title)
    #     print(i.head0)
    params={'blog':blogs}
    return render(request,'blog/index.html',params)

def blogpost(request,myid):
    blogs = BlogPost.objects.filter(post_id=myid)
    # for i in blogs:
    # print(blogs[0].title)

    return render(request,'blog/blogpost.html',{'blog':blogs[0]})
