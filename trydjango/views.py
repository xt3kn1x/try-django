from django.http import HttpResponse
from django.template.loader import render_to_string
from articles.models import Article
import random

def home_view(request):

    random_id = random.randint(1, 2)
    article_obj = Article.objects.get(id=random_id)
    article_qs = Article.objects.all()

    context = {
        "object_list": article_qs,
        "title": article_obj.title,
        "content": article_obj.content
    }

    HTML_STRING = render_to_string('home-view.html', context=context)


    return HttpResponse(HTML_STRING)