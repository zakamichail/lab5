from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http import Http404

from .models import Article



def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    # Посколько механизм авторизации будет реализован только в 6
    # лабораторной работе, пока выключим проверку

    # if request.user.is_anonymous:
    #     raise Http404

    if request.method == "GET":
        return render(request, "create_post.html", {})

    form = {"text": request.POST["text"], "title": request.POST["title"]}

    if not (form["text"] and form["title"]):
        form["errors"] = "Не все поля заполнены"
        return render(request, "create_post.html", {"form": form})

    if Article.objects.filter(title=form["title"]).exists():
        form["errors"] = "Статья с таким заголовком существует"
        return render(request, "create_post.html", context={"form": form})

    # временное решение
    user = User.objects.get(username="zakamichail")
    
    article = Article.objects.create(
        text=form["text"], title=form["title"], author=user
    )
    return redirect("get_article", article_id=article.id)