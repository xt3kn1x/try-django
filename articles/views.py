from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from .forms import ArticleForm
from .models import Article

# Create your views here.

def article_search_view(request):
    query = request.GET.get('query') # This is a dictionary of the GET request : print(request.GET)
    print(request.GET.get('query'))
    # article_detail_obj = None
    # if query is not None:
    #     article_detail_obj = Article.objects.get(id=query)
    # Converting from Object to Query set.
    qs = Article.objects.all()
    if query is not None:
        qs = Article.objects.search(query) # This is a way to omit the previous two lines.
    context = {
        "object_list": qs
    }
    return render(request, 'articles/search.html', context=context)

@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    # print(dir(form))
    context = {
        "form": form
    }
    if form.is_valid():
        article_object = form.save()
        context['form'] = ArticleForm()
        # return redirect("article-detail", slug=article_object.slug)
        return redirect(article_object.get_absolute_url())
        # title = form.cleaned_data.get("title")
        # content = form.cleaned_data.get("content")
        # article_object = Article.objects.create(title=title, content=content)
        # context['object'] = article_object
        # context['created'] = True
    if request.htmx:
        return render(request, "articles/partials/forms.html", context)
    return render(request, 'articles/create.html', context=context)
    # form = ArticleForm()
    # print(dir(form))
    # context = {
    #     "form": form
    # }
    # if request.method == "POST":
    #     form = ArticleForm(request.POST)
    #     context['form'] = form
    #     if form.is_valid():
    #         title = form.cleaned_data.get("title")
    #         content = form.cleaned_data.get("content")
    #         article_object = Article.objects.create(title=title, content=content)
    #         context['object'] = article_object
    #         context['created'] = True
    # return render(request, 'articles/create.html', context=context)

def home_view_detail(request, slug=None):
    article_detail_obj = None
    if slug is not None:
        try:
            article_detail_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_detail_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        "object": article_detail_obj
    }
    return render(request, 'articles/view-detail.html', context=context)