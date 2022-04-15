from django.contrib.auth.models import auth
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from . import forms
from . import models
from comments .forms import CommentForm

PERPAGE = 5
PAGECOUNT = 5

def cal_page(page_obj, paginator):
    page_num = PAGECOUNT
    half = page_num // 2
    pre_list = [x for x in range(page_obj.number - half, page_obj.number) if x >= 1]
    next_list = [x for x in range(page_obj.number + 1, page_obj.number + half + 1) if x <= paginator.num_pages]

    return {'pre_list': pre_list, 'next_list': next_list}

#ListView DetailView TemplateView
class homepageView(ListView):
    model = models.Bloginfo
    template_name = 'project/homepage.html'
    context_object_name = "blog_list"
    paginate_by = PERPAGE     # how many bolg shows in a page

    def get_context_data(self, **kwargs):
        context = super(homepageView, self).get_context_data()
        page_data = cal_page(context.get('page_obj'), context.get('paginator'))
        context.update(page_data)
        return context


class categoryView(ListView):
    model = models.Bloginfo
    template_name = 'project/category.html'
    context_object_name = "blog_list"
    paginate_by = PERPAGE     # how many blog shows in a page


    #not all blogs, but category, like sql: where category='xxx'
    def get_queryset(self):
        category_id = self.kwargs.get('categoryid')
        category = get_object_or_404(models.Category, pk=category_id)
        return super(categoryView, self).get_queryset().filter(category=category).order_by("-created_time")

    def get_context_data(self, **kwargs):
        context = super(categoryView, self).get_context_data()
        context['category'] = get_object_or_404(models.Category, pk=self.kwargs.get('categoryid'))
        page_data = cal_page(context.get('page_obj'), context.get('paginator'))
        context.update(page_data)
        return context

class tagView(ListView):
    model = models.Bloginfo
    template_name = 'project/tags.html'
    context_object_name = "blog_list"
    paginate_by = PERPAGE     # how many bolg shows in a page


    #not all blogs, but category, like sql: where category='xxx'
    def get_queryset(self):
        tag_id = self.kwargs.get('tagid')
        tag = get_object_or_404(models.Tag, pk=tag_id)
        return super(tagView, self).get_queryset().filter(tags=tag).order_by("-created_time")

    def get_context_data(self, **kwargs):
        context = super(tagView, self).get_context_data()
        context['tags'] = get_object_or_404(models.Tag, pk=self.kwargs.get('tagid'))
        page_data = cal_page(context.get('page_obj'), context.get('paginator'))
        context.update(page_data)
        return context

class authorPage(ListView):
    model = models.Bloginfo
    template_name = 'project/authorPage.html'
    context_object_name = "blog_list"
    paginate_by = PERPAGE     # how many bolg shows in a page


    #not all blogs, but category, like sql: where category='xxx'
    def get_queryset(self):
        author_id = self.kwargs.get('userid')
        author = get_object_or_404(models.RegisterUser, pk=author_id)
        return super(authorPage, self).get_queryset().filter(author=author).order_by("-created_time")

    def get_context_data(self, **kwargs):
        context = super(authorPage, self).get_context_data()
        context['author'] = get_object_or_404(models.RegisterUser, pk=self.kwargs.get('userid'))
        page_data = cal_page(context.get('page_obj'), context.get('paginator'))
        context.update(page_data)
        return context

class blogDetail(DetailView):
    model = models.Bloginfo
    template_name = 'project/blogDetail.html'
    context_object_name = "blog"
    pk_url_kwarg = 'blogid'

    def get_object(self, queryset=None):
        blog = super(blogDetail, self).get_object(queryset=None)
        blog.add_one_view()
        return blog

    def get_context_data(self, **kwargs):
        context = super(blogDetail, self).get_context_data()
        form = CommentForm()

        context['form'] = form
        comments_list = self.object.comment_set.all()
        context['comment_list'] = comments_list
        return context



def register(request):
    if request.method == 'POST':
        """
        user register view method
        """
        form_obj = forms.reg_form(request.POST, request.FILES)
        if form_obj.is_valid():
            #confirm password
            form_obj.cleaned_data.pop('repassword')
            #use django to create a new user, and store the data that entered in the web to our database
            user_obj = models.RegisterUser.objects.create_user(**form_obj.cleaned_data, is_staff=1, is_superuser=1)

            #auto login after register
            auth.login(request, user_obj)

            #jump to the main page
            return redirect("/")
        else:
            return render(request, "project/register.html", {'formobj': form_obj})

    else:
        #combine the forms.py with the webpage
        form_obj = forms.reg_form()
        return render(request, "project/register.html",{'formobj': form_obj})


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #use auth check user
        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)

            # jump to main page
            return redirect("/")
        else:
            return render(request, "project/login.html", {'error': "username or password is incorrect!"})
    else:
        return render(request, "project/login.html")

def login_ajax(request):
    ret = {
        "code": 0,
        "message": "ok"
    }
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        #use auth check user
        user = auth.authenticate(username=username, password=password)

        if user:
            auth.login(request, user)
        else:
            ret['code'] = 999
            ret['message'] = "username or password is incorrect!"
    else:
        ret['code'] = -1
        ret['message'] = "illegal request."

    return JsonResponse(ret)

def logout(request):
    auth.logout(request)

    return redirect("/")

def archives(request, month, year):
    #archive blogs count

    blog_list = models.Bloginfo.objects.filter(created_time__month=month,
                                               created_time__year=year).order_by("-created_time")
    return render(request, "project/archives.html", {'blog_list': blog_list, 'month': month, 'year': year})


def likes(request):
    ret = {'code': 0, 'message': 'ok'}

    blogid = request.GET.get('blogid')

    project = models.Bloginfo.objects.get(id=blogid)
    if project:
        # likes add one
        project.add_one_like()


    return JsonResponse(ret)
