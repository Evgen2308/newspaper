from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

# # для проставления лайков/дислайков. НЕ ОБЯЗАТЕЛЬНО
# import random


def to_make():
    # полезно для отладки удалять объекты
    User.objects.all().delete()
    Category.objects.all().delete()

    # создание пользователей
    alex_user = User.objects.create_user(username='alex', email='alex@mail.ru', password='alex_password')
    tom_user = User.objects.create_user(username='tom', email='tom@mail.ru', password='tom_password')

    # создание объектов авторов
    alex = Author.objects.create(user=alex_user)
    tom = Author.objects.create(user=tom_user)

    # создание категорий
    cat_sport = Category.objects.create(name="Спорт")
    cat_music = Category.objects.create(name="Музыка")
    cat_cinema = Category.objects.create(name="Кино")
    cat_IT = Category.objects.create(name="IT")

    # создание текстов статей/новостей
    text_article_sport_cinema = """статья_спорт_кино_Алекса__статья_спорт_кино_Алекса__статья_спорт_кино_Алекса_
                                   _статья_спорт_кино_Алекса__статья_спорт_кино_Алекса__"""

    text_article_music = """статья_музыка_Тома__статья_музыка_Тома__статья_музыка_Тома_
                            _статья_музыка_Тома__статья_музыка_Тома__"""

    text_news_IT = """новость_IT_Тома__новость_IT_Тома__новость_IT_Тома__новость_IT_Тома__
                    новость_IT_Тома__новость_IT_Тома__новость_IT_Тома__новость_IT_Тома__"""

    # создание двух статей и новости
    article_alex = Post.objects.create(author=alex, post_type=Post.article, title="статья_спорт_кино_Алекса",
                                        text=text_article_sport_cinema)
    article_tom = Post.objects.create(author=tom, post_type=Post.article, title="статья_музыка_Тома",
                                        text=text_article_music)
    news_tom = Post.objects.create(author=tom, post_type=Post.news, title="новость_IT_Тома", text=text_news_IT)

    # присваивание категорий этим объектам
    PostCategory.objects.create(post=article_alex, category=cat_sport)
    PostCategory.objects.create(post=article_alex, category=cat_cinema)
    PostCategory.objects.create(post=article_tom, category=cat_music)
    PostCategory.objects.create(post=news_tom, category=cat_IT)

    # создание комментариев
    comment1 = Comment.objects.create(post=article_alex, user=tom.user, text="коммент Тома №1 к статье Алекса")
    comment2 = Comment.objects.create(post=article_tom, user=alex.user, text="коммент Алекса №2 к статье Тома")
    comment3 = Comment.objects.create(post=news_tom, user=tom.user, text="коммент Тома №3 к новости Тома")
    comment4 = Comment.objects.create(post=news_tom, user=alex.user, text="коммент Алекса №4 к новости Тома")

    # список всех объектов, которые можно лайкать
    list_for_like = [article_alex,
                     article_tom,
                     news_tom,
                     comment1,
                     comment2,
                     comment3,
                     comment4]

    # 100 рандомных лайков/дислайков
    for i in range(100):
        random_obj = random.choice(list_for_like)
        if i % 2:
            random_obj.like()
        else:
            random_obj.dislike()

    # подсчет рейтинга Алекса
    rating_alex = (sum([post.rating * 3 for post in Post.objects.filter(author=alex)])
                    + sum([comment.rating for comment in Comment.objects.filter(user=alex.user)])
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=alex)]))
    alex.update_rating(rating_alex)  # и обновление

    # подсчет рейтинга Тома
    rating_tom = (sum([post.rating * 3 for post in Post.objects.filter(author=tom)])
                    + sum([comment.rating for comment in Comment.objects.filter(user=tom.user)])
                    + sum([comment.rating for comment in Comment.objects.filter(post__author=tom)]))
    tom.update_rating(rating_tom)  # и обновление

    # лучший автор
    best_author = Author.objects.all().order_by('-rating')[0]

    print("Лучший автор")
    print("username:", best_author.user.username)
    print("Рейтинг:", best_author.rating)
    print("")

    # лучшая статья(!) - именно статья (ВАЖНО)
    best_article = Post.objects.filter(post_type=Post.article).order_by('-rating')[0]
    print("Лучшая статья")
    print("Дата:", best_article.created)
    print("Автор:", best_article.author.user.username)
    print("Рейтинг:", best_article.rating)
    print("Заголовок:", best_article.title)
    print("Превью:", best_article.preview())
    print("")

    # печать комментариев к ней. Обязательно цикл, потому что комментарий может быть не один и нужен универсальный код
    print("Комментарии к ней")
    for comment in Comment.objects.filter(post=best_article):
        print("Дата:", comment.created)
        print("Автор:", comment.user.username)
        print("Рейтинг:", comment.rating)
        print("Комментарий:", comment.text)
        print("")