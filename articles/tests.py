from django.test import TestCase
from .models import Article

# Create your tests here.

class ArticleTestCase(TestCase):
    def setUp(self):
        for i in range(0, 5):
            Article.objects.create(title='Hello world', content='something else')

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertTrue(qs.count(), 5)