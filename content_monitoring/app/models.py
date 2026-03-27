from django.db import models

# Create your models here.
class Keyword(models.Model):
    name=models.TextField(max_length=255)
    def __str__(self):
        return self.name
class ContentItem(models.Model):
    title=models.CharField(max_length=200)
    body=models.TextField()
    source=models.CharField(max_length=100)
    last_updated=models.DateTimeField()
    def __str__(self):
        return self.title
class Flag(models.Model):
    STATUS_CHOICES=[('pending', 'Pending'),
        ('relevant', 'Relevant'),
        ('irrelevant', 'Irrelevant'),]
    keyword=models.ForeignKey(Keyword,on_delete=models.CASCADE)
    content_item=models.ForeignKey(ContentItem,on_delete=models.CASCADE)
    score=models.IntegerField()
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='pending')
    reviewed_at=models.DateTimeField(null=True,blank=True)
    def __str__(self):
        return f"{self.keyword}-{self.content_item} {self.status}"
