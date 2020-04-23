from rest_framework import serializers


class SingleArticleSerializer(serializers.Serializer):
    title = serializers.CharField(required=True,
                                  max_length=128,
                                  allow_null=False,
                                  allow_blank=False)
    cover = serializers.CharField(required=True,
                                  max_length=256,
                                  allow_null=False,
                                  allow_blank=False)
    content = serializers.CharField(required=True,
                                  max_length=2048,
                                  allow_null=False,
                                  allow_blank=False)
    created_at = serializers.CharField(required=True,
                                  allow_null=False,
                                  allow_blank=False)


class SubmitArticleSerializer(serializers.Serializer):
    title = serializers.CharField(required=True,
                                  max_length=128,
                                  allow_null=False,
                                  allow_blank=False)
    cover = serializers.FileField(required=True,
                                  allow_null=False,
                                  allow_empty_file=False)
    content = serializers.CharField(required=True,
                                    max_length=2048,
                                    allow_null=False,
                                    allow_blank=False)
    category_id = serializers.IntegerField(required=True,
                                       allow_null=False)
    author_id = serializers.IntegerField(required=True,
                                       allow_null=False)
    promoted = serializers.BooleanField(required=True,
                                         allow_null=False)


class UpdateCoverArticleSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True,
                                          allow_null=False)
    cover = serializers.FileField(required=True,
                                  allow_null=False,
                                  allow_empty_file=False)


class DeleteArticleSerializer(serializers.Serializer):
    article_id = serializers.IntegerField(required=True,
                                          allow_null=False)