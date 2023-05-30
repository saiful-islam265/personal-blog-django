from django.shortcuts import render, get_object_or_404
from .models import Article
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag


# Create your views here.
def list_of_articles(request, tag_slug = None):
    articles = Article.publishedArticles.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        articles = articles.filter(tags__in=[tag])

    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page', 1)
    try:
        articles = paginator.page(page_number)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        articles = paginator.page(1)

    return render(request, 'blog/list.html', {'articles': articles, 'tag': tag})
    pass


def article_details(request, id):
    try:
        article = get_object_or_404(Article, id=id, status=Article.Status.PUBLISHED)
    except Article.DoesNotExist:
        raise Http404("No article found.")

    return render(request, 'blog/detail.html', {'article': article})
    pass