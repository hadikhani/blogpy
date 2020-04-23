from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import serializers

class IndexPage(TemplateView):

    def get(self, request, **kwargs):
        article_data = []

        all_article = Article.objects.all().filter(promoted=False).order_by('-created_at')[:9]
        for article in all_article:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.date(),
            })

        promoted_article_data = []
        all_promoted_article = Article.objects.all().filter(promoted=True)
        for promoted in all_promoted_article:
            promoted_article_data.append({
                'title': promoted.title,
                'cover': promoted.cover.url,
                'category': promoted.category.title,
                'created_at': promoted.created_at.date(),
                'avatar': promoted.author.avatar.url,
                'author_name': promoted.author.user.first_name + ' ' + promoted.author.user.last_name
            })
        context = {
            'article_data': article_data,
            'promoted_article_data': promoted_article_data,
        }

        return render(request, 'index.html', context)


class ContactPage(TemplateView):
    template_name = 'page-contact.html'


class AllArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            all_articles = Article.objects.all().order_by('created_at')[:10]
            data = []

            for article in all_articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url,
                    'content': article.content,
                    'created_at': article.created_at,
                    'category': article.category.title,
                    'author': article.author.user.first_name + ' ' + article.author.user.last_name,
                    'promoted': article.promoted,
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serialized_data = serializers.SingleArticleSerializer(article, many=True)
            data = serialized_data.data
            return Response({'data': data},status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchArticleAPIView(APIView):
    def get(self, request, format=None):
        try:
            from django.db.models import Q
            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            data = []
            for article in articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url,
                    'content': article.content,
                    'created_at': article.created_at,
                    'category': article.category.title,
                    'author': article.author.user.first_name + ' ' + article.author.user.last_name,
                    'promoted': article.promoted,
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'data':"Internal server error, We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubmitArticleAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = serializers.SubmitArticleSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = request.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promoted = serializer.data.get('promoted')
            else:
                return Response({'status': 'Bad Request.'},
                                status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user=user)
            category = Category.objects.get(id=category_id)

            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promoted = promoted
            article.save()
            return Response({'status': 'OK'},
                            status=status.HTTP_200_OK)

        except:
            return Response({'data': "Internal server error, We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateCoverArticleAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = serializers.UpdateCoverArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response({'status': 'Bad Request.'},
                                status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).update(cover=cover)

            return Response({'status': 'OK'},
                            status=status.HTTP_200_OK)
        except:
            return Response({'data': "Internal server error, We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):
    def post(self, request, format=None):
        try:
            serializer = serializers.DeleteArticleSerializer(data=request.data)
            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
            else:
                return Response({'status': 'Bad Request.'},
                                status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).delete()

            return Response({'status': 'OK'},
                            status=status.HTTP_200_OK)
        except:
            return Response({'data': "Internal server error, We'll check it later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)