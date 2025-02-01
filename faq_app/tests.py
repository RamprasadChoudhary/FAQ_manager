from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIClient
from .models import FAQ

class FAQTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a high-level Python web framework."
        )

    def test_faq_model(self):
        self.assertEqual(str(self.faq), "What is Django?")

    def test_faq_api(self):
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_faq_translation(self):
        response = self.client.get('/api/faqs/?lang=hi')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data[0]['question'], "What is Django?")
    
    def test_faq_creation(self):
        faq_count = FAQ.objects.count()
        new_faq = FAQ.objects.create(
            question="What is Python?",
            answer="Python is a high-level programming language."
        )
        self.assertEqual(FAQ.objects.count(), faq_count + 1)
        self.assertEqual(str(new_faq), "What is Python?")

    def test_faq_update(self):
        self.faq.question = "What is Django framework?"
        self.faq.save()
        updated_faq = FAQ.objects.get(id=self.faq.id)
        self.assertEqual(str(updated_faq), "What is Django framework?")

    def test_faq_deletion(self):
        faq_count = FAQ.objects.count()
        self.faq.delete()
        self.assertEqual(FAQ.objects.count(), faq_count - 1)

    def test_faq_api_languages(self):
        for lang in ['en', 'hi', 'bn']:
            response = self.client.get(f'/api/faqs/?lang={lang}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.data), 1)
            self.assertIn('question', response.data[0])
            self.assertIn('answer', response.data[0])

        