from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage #to paginate our queryset on django
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect,reverse
from .models import Post, Author, PostView
from marketing.models import SignUp
from .forms import CommentForm,PostForm

queryset = Post.objects.all()


def get_author(user):
    qs = Author.objects.filter(user=user)
    # print(qs.Author.user)
    if qs.exists():
        return qs[0]
    return None


def search(request):
    queryset = Post.objects.all()
    print(queryset)
    query = request.GET.get('q')
    if query:
        #here special fun. is used i.e Q with the help of which we are filtering our databases posts by the entered query.
        queryset = queryset.filter(
            Q(title__icontains = query) | Q(overview__icontains = query)
        ).distinct() #.distinct() to return different post.
    print(queryset)
    
    context = {
        "queryset" : queryset,
    }
    return render(request, "search_results.html",context)


def get_category_count():
    #fun. that will count how many post have same category of posts.
    queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset


def index(request):
    #logic for latest blog.
    featured = Post.objects.filter(featured = True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    #logic for subscription of email.
    if request.method == "POST":
        email = request.POST["email"]
        new_signup = SignUp()
        new_signup.email = email
        new_signup.save()


    context = {
        'object_list':featured,
        'latest':latest,
    }

    return render(request, "index.html",context) 


def blog(request):
    category_count = get_category_count()
    # print(category_count)
    post_list = Post.objects.all() #line to get all post from DB.

    #
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    
    #logic for paginator
    paginator = Paginator(post_list,4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)


    context = {
        'queryset':paginated_queryset,
        'most_recent':most_recent,
        'page_request_var':page_request_var,
        'category_count':category_count,
    }
    return render(request, "blog.html",context) 



def post(request, id):
    # title = "Create"
    post = get_object_or_404(Post, id=id)
    #you can also creaet another view to keep track of anonymous view user
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user,post=post)
    most_recent = Post.objects.order_by('-timestamp')[0:3]
    category_count = get_category_count()

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail",kwargs={
                'id': post.pk,
            })) 
    context = {
        'form':form,
        # 'title':title, 
        'post':post,
        'most_recent':most_recent,
        'category_count':category_count,

    }
    
    return render(request, "post.html",context) 

def post_create(request):
    title = "Create "
    form = PostForm(request.POST or None, request.FILES or None)
    print("user-", request.user)
    author = get_author(request.user)
    # # TODO: Solve the error
    # print("Hey-",author)

    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail",kwargs={
                'id': form.instance.id,
            })) 
    context = {
        'form':form,
        'title':title,
    }
    return render(request, "post_create.html", context)


def post_update(request, id):
    title = "Update "
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None,instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail",kwargs={
                'id': form.instance.id,
            })) 
    context = {
        'title':title,
        'form':form,
    }
    return render(request, "post_create.html", context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list") )

