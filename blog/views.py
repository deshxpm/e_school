from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from classroom.models import Category
from .models import Post, PostAuthor, Tag, Image
from.forms import CreatePostForm,UpdatePostForm,CreateInternshipForm
# Create your views here.

def blog_home(request):
    blogs=Post.objects.all()
    context={
        'objects':blogs
    }
    return render(request,'blog/blog_home.html',context)

def post_Details(request,id):
    # cats = Category.objects.all()
    # tags = Tag.objects.all()

    post = get_object_or_404(Post, id=id)
    context={
        'object':post
    }
    return render(request,'blog/blog_detail.html',context)

@login_required
def createPost(request):
    user=request.user
    author_=PostAuthor.objects.get(user=user)
    form=CreatePostForm()
    if request.method=="POST":
        form=CreatePostForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            new_post=form.save(commit=False)
            new_post.author=author_
            new_post.save()
            return redirect('blog_details',new_post.id)
    context={
        'form':form
    }
    return  render(request,'blog/blog_create.html',context)

@login_required
def updatePost(request,id):
    user=request.user
    author_ = PostAuthor.objects.get(user=user)
    post=Post.objects.get(id=id)
    form=UpdatePostForm()
    if request.method=="POST":
        form=UpdatePostForm(request.POST or None,request.FILES or None,instance=post)
        if form.is_valid():
            post_=form.save(commit=False)
            post_.save()
        return redirect('blog_details',id)
    form=UpdatePostForm(
        initial={
            "title": post.title,
            "content": post.content,
            "thumbnail": post.thumbnail,
        }
    )
    context={
        "form":form
    }
    return render(request,'blog/blog_update.html',context)

def delete_post(request,id):
    user=request.user
    # author_ = PostAuthor.objects.get(user=user)
    post = Post.objects.get(id=id)

    if post.author.user != request.user:
        # messages.warning(request, "Restricted ..!")
        return redirect('post',id=id)
    post.delete()
    # messages.success(request, f"{post.title} is successfully deleted ")
    return redirect('blogs')


@login_required
def add_internShip(request):
    user = request.user
    author_=PostAuthor.objects.get(user=user)
    form = CreateInternshipForm()
    if request.method == "POST":
        form = CreateInternshipForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_internship = form.save(commit=False)
            new_internship.author = author_
            new_internship.save()
            return redirect('internships-detail', new_internship.id)
    context = {
        'form': form
    }
    return render(request, 'blog/internship_create.html', context)


