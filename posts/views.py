from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from .models import Category, Post, Comment
from .forms import CommentForm

from django.contrib.auth.decorators import login_required

# Create your views here.
def base(request):
    return render(request, 'base.html')

def main(request):
    return render(request, 'main.html')


def cate_detail(request, cate_id):
    '''
    카테고리 디테일
    1) 작성자가 같아야 함
    2) 카테고리가 같아야 함
    3) 글 내용이 같아야 함
    4) 글 아이디가 같아야 함 ✔
    '''

    # 해당 카테고리 글 다 가져오기
    # posts = get_object_or_404(Category, id=id) #이렇게 하면 html에서 반복을 못함
    posts = Post.objects.filter(post_cate=cate_id)

    # 각 글의 content, comment, img, author, date 가져오기(모달부분)

    context = {
        'posts':posts,
    }
    return render(request, 'category_detail.html', context)

'''
1. 해당 카테고리 글 다 가져옴
1-2. cate_detail에 글 보이기
2. 더보기를 누르면 comment view 실행
2-2. 각 글에 해당하는 댓글 다 가져옴 (Post id==Comment id)
3. 닫기를 누르면 댓글 사라짐.
'''

def cate_detail_comment(request, cate_id, post_id):
    posts = Post.objects.filter(post_cate=cate_id)
    post = get_object_or_404(Post, pk=post_id)
    # cate_id = post.post_cate
    # print('cate_id 잘 가져 오고 있느냐 :: ', cate_id)
    # posts = Post.objects.filter(post_cate=cate_id)
    cmts = Comment.objects.filter(post_id=post_id)
    '''댓글'''
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post_id = request.post_id
            comment.comment_content = comment_form.cleaned_data['comment_content']
            comment.comment_date = timezone.now()
            comment.save()
            return redirect('cate_detail')
    else:
        comment_form = CommentForm()
        context = {
            'posts':posts,
            'post':post,
            'cmt_form':comment_form,
            'cmts':cmts
        }
        return render('category_detail.html', context)

def category(request):
    '''카테고리 육각형 모음'''
    cates = Category.objects.all() #objects까지만 쓰면 'Manager'에 접근 못한다는 오류 뜸
    return render(request, 'category.html' ,{'cates':cates})

def write(request):
    '''if request.method == 'POST':'''
    post = Post()
    post.author = request.user
    post.post_date = timezone.now()
    post.post_content = request.POST.get('post_content')
    post.post_img = request.FILES.get('post_img')
    post_cate_id = request.POST.get('post_cate') #cate의 id를 가져옴
    print("cate id 출력해보기 :: ", post_cate_id)
    post.post_cate = Category.objects.get(id=post_cate_id) #cate의 id에 해당하는 Category모델에서 object를 불러와봤는데 디비에저장된이름(한글) 그대로 옴

    # post.post_cate = request.POST.get('post_cate')
    post.save() 
    return redirect('cate_detail', post_cate_id)

    '''이 밑에 방법으로 해봤는데 url이 /category/id/가 아니라 write로 됐음'''
    # posts = Post.objects.filter(post_cate=post_cate_id)
    # return render(request, 'category_detail.html', {'posts':posts})
    
def get_write(request):
    '''if request.method=='GET:'''
    post_cate = Category.objects.all()
    return render(request, 'write.html', {'post_cate':post_cate})

def edit(request, id):
    edit_post = Post.objects.filter(id=id)
    if request.method == 'POST':
        post = Post()
        user = request.user
        post.author = user
        return redirect('mypage', user.id)
    else:
        return render(request, 'edit.html', {'edit_post':edit_post, 'post':post, 'user':user})
        
def update(request, id):
    update_post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        update_post.post_date = timezone.now()
        update_post.post_content = request.POST['post_content']
        update_post.post_img = request.FILES.get('post_image')
        update_post.save()
        return redirect('mypage', update_post.id)
    else:
        return render(request, 'edit.html')


def delete (request, id):
    if request.method == 'GET':
        delete_post = get_object_or_404(Post, id=id)
        post = Post()
        user = request.user
        post.author = user
        delete_post.delete()
    return redirect('mypage', user.id)
    
# 좋아요
def likes(request, id):
    like_post = get_object_or_404(Post, id=id)
    if request.user in like_post.like.all():
        like_post.like.remove(request.user)
        like_post.like_count -= 1
        like_post.save()
    else:
        like_post.like.add(request.user)
        like_post.like_count += 1
        like_post.save()
    return redirect('/posts/category_detail/category/' + str(id))

# category_detail
def gardening(request):
    return render(request, 'category_detail/gardening.html')

def farming(request, farming):
    category = Post.objects.filter(category=farming)
    return render(request, 'category_detail/farming.html', {'category':category})

def yoga(request, yoga):
    category = Post.objects.filter(category=yoga)
    return render(request, 'category_detail/yoga.html',{'category':category})

# def bicycle(request, cate):
#     # category_posts = posts.filter(post_cate='자전거')
#     return render(request, 'category_detail/bicycle.html', cate)

def cooking(request, cooking):
    category = Post.objects.filter(category=cooking)
    return render(request, 'category_detail/cooking.html', {'category':category})

def go(request, go):
    category = Post.objects.filter(category=go)
    return render(request, 'category_detail/go.html', {'category':category})

def hiking(request, hiking):
    category = Post.objects.filter(category=hiking)
    return render(request, 'category_detail/hiking.html', {'category':category})

def knitting(request, knitting):
    category = Post.objects.filter(category=knitting)
    return render(request, 'category_detail/knitting.html', {'category':category})

def fishing(request, fishing):
    category = Post.objects.filter(category=fishing)
    return render(request, 'category_detail/fishing.html', {'category':category})