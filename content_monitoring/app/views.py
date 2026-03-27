from rest_framework import viewsets
from rest_framework.response import Response
from .models import Keyword, Flag,ContentItem
from .serializer import KeywordSerializer, FlagSerializer
from rest_framework.decorators import api_view
from django.utils import timezone


class KeywordViewSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer


class FlagViewSet(viewsets.ModelViewSet):
    queryset = Flag.objects.all()
    serializer_class = FlagSerializer


@api_view(['POST'])
def scan(request):
    keywords = Keyword.objects.all()
    contents = ContentItem.objects.all()

    for content in contents:
        for keyword in keywords:
            k = keyword.name.lower()
            title = content.title.lower()
            body = content.body.lower()

            # 🎯 SCORING LOGIC
            if k == title:
                score = 100
            elif k in title:
                score = 70
            elif k in body:
                score = 40
            else:
                continue

            # 🔥 SUPPRESSION LOGIC
            existing = Flag.objects.filter(keyword=keyword, content_item=content).first()

            if existing:
                if existing.status == "irrelevant":
                    if content.last_updated > (existing.reviewed_at or timezone.now()):
                        existing.score = score
                        existing.status = "pending"
                        existing.save()
                continue

            # Create new flag
            Flag.objects.create(
                keyword=keyword,
                content_item=content,
                score=score
            )

    return Response({"message": "Scan completed"})