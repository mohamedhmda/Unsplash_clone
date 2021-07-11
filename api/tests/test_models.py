from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User
from api.models import Image, Like, Collection, Follower

##
## python manage.py test --verbosity 2
## 

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="test_user",
            first_name = "mohamed",
            last_name = "hamaida",
            email = "mohamed@gmail.com",
            password="123456789abc"
            )

    def test_get_absolute_url(self):
        user = User.objects.get(pk = 1)
        self.assertEqual(user.get_absolute_url(), '/profile/1')
    
    def test_create_existing_user(self):
        user, created = User.objects.get_or_create(
            username="test_user",
            first_name = "mohamed",
            last_name = "hamaida",
            email = "mohamed@gmail.com",
            password = "123456789abc"
            )
        
        self.assertFalse(created)

class ImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="test_user",
            first_name = "mohamed",
            last_name = "hamaida",
            email = "mohamed@gmail.com",
            password="123456789abc"
            )
        
        number_of_images = 2
        for image in range(number_of_images):
            im = Image.objects.create(
                user = user,
                description = "race week",
                photo = "https://i.ibb.co/jRJ5QxW/1a53d3ee1504.jpg",
                location = "monaco"
            )
            im.tags.add("f1","monaco")
    
    def test_get_absolute_url(self):
        image = Image.objects.first()
        self.assertEqual(image.get_absolute_url(), '/image/1')

    def test_default_like_is_zero(self):
        image = Image.objects.first()
        self.assertEqual(image.likes, 0)

class LikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="test_user",
            first_name = "mohamed",
            last_name = "hamaida",
            email = "mohamed@gmail.com",
            password="123456789abc"
            )

        number_of_images = 2
        for image in range(number_of_images):
            im = Image.objects.create(
                user = user,
                description = "race week",
                photo = "https://i.ibb.co/jRJ5QxW/1a53d3ee1504.jpg",
                location = "monaco"
            )
            im.tags.add("f1","monaco")

    def test_like_image(self):
        user = User.objects.first()
        image = Image.objects.first()

        login = self.client.force_login(user, backend=None)
        response = self.client.get(reverse('api:likeimage', kwargs={'image_id' : image.id}))
        self.assertRedirects(response, reverse('api:image', kwargs={'pk' : image.id}))

        #self.assertEqual(image.likes, 1)

    
