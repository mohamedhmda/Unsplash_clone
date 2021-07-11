from os import name
from django.test import TestCase
from django.test import Client
from django.urls import reverse

from django.contrib.auth.models import User
from api.models import Collection, Image,Like


""" Home view """
class HomeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_images = 2
        user = User.objects.create(
            username="test_user",
            first_name = "mohamed",
            last_name = "hamaida",
            email = "mohamed@gmail.com",
            password = "123456789abc"
            )

        for image in range(number_of_images):
            im = Image.objects.create(
                user = user,
                description = "race week",
                photo = "https://i.ibb.co/jRJ5QxW/1a53d3ee1504.jpg",
                location = "monaco"
            )
            im.tags.add("f1","monaco")

    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('api:home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('api:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/index.html')

    def test_lists_all_images(self):
        number_of_images = 2
        response = self.client.get(reverse('api:home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['Images']), number_of_images)


class ImageDetailViewTest(TestCase):
    def setUp(self):
        number_of_images = 2
        user = User.objects.create(
            username="test_user",
            first_name = "mohamed",
            last_name = "hamaida",
            email = "mohamed@gmail.com",
            password="123456789abc"
            )
        for image in range(number_of_images):
            im = Image.objects.create(
                user = user,
                description = "race week",
                photo = "https://i.ibb.co/jRJ5QxW/1a53d3ee1504.jpg",
                location = "monaco"
            )
            im.tags.add("f1","monaco")
        
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/image/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        image = Image.objects.first()
        response = self.client.get(reverse('api:image',kwargs={'pk' : image.id}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        image = Image.objects.first()
        response = self.client.get(reverse('api:image',kwargs={'pk' : image.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/image_detail.html')

    def test_user_loged_in(self):
        user = User.objects.first()
        login = self.client.force_login(user , backend=None)
        response = self.client.get(reverse('api:home'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), user.username)
        self.assertEqual(response.status_code, 200)
    
    def test_like_image_with_not_logged_in_user(self):
        image = Image.objects.first()
        response = self.client.get(reverse('api:likeimage', kwargs={'image_id' : image.id}))
        self.assertNotEqual(response.status_code, 200)

    def test_like_image_with_logged_in_user(self):
        image = Image.objects.first()
        user = User.objects.first()
        login = self.client.force_login(user, backend=None)
        response = self.client.get(reverse('api:likeimage', kwargs={'image_id' : image.id}))
        self.assertRedirects(response, reverse('api:image', kwargs={'pk' : image.id}))

    def test_like_liked_image(self):
        image = Image.objects.first()
        user = User.objects.first()
        login = self.client.force_login(user, backend=None)
        # first like it
        response = self.client.get(reverse('api:likeimage', kwargs={'image_id' : image.id}))
        # like it again
        response2 = self.client.get(reverse('api:likeimage', kwargs={'image_id' : image.id}))
        self.assertEqual(response2.status_code, 404)
        
    
    def test_unlike_image_with_not_logged_in_user(self):
        image = Image.objects.first()
        response = self.client.get(reverse('api:unlikeimage', kwargs={'image_id' : image.id}))
        self.assertNotEqual(response.status_code, 200)

    def test_unlike_image_with_not_logged_in_user(self):
        image = Image.objects.first()
        user = User.objects.first()
        login = self.client.force_login(user, backend=None)
        response = self.client.get(reverse('api:unlikeimage', kwargs={'image_id' : image.id}))
        if Like.objects.filter(image_id=image.id, user_id=user.id).exists():
            self.assertRedirects(response, reverse('api:image', kwargs={'pk' : image.id}))
        else:
            self.assertEqual(response.status_code, 404)


    def test_delete_image_with_loged_in_user(self):
        image = Image.objects.first()
        user = User.objects.first()
        login = self.client.force_login(user, backend=None)
        response = self.client.get(reverse('api:deleteimage', kwargs={'image_id' : image.id}))
        self.assertRedirects(response, reverse('api:profile', kwargs={'pk' : user.id}))

    def test_delete_image_with_not_loged_in_user(self):
        image = Image.objects.first()
        user = User.objects.first()
        response = self.client.get(reverse('api:deleteimage', kwargs={'image_id' : image.id}))
        url = reverse('account_login')+"?next=/deleteimage/1"
        self.assertRedirects(response, url)

    def test_delete_non_existing_image(self):
        user = User.objects.first()
        login = self.client.force_login(user, backend=None)
        response = self.client.get(reverse('api:deleteimage', kwargs={'image_id' : 25}))
        self.assertEqual(response.status_code, 404)


class SearchView(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_images = 2
        user = User.objects.create(
            username="test_user",
            first_name = "mohamed",
            last_name = "hamaida",
            email = "mohamed@gmail.com",
            password = "123456789abc"
            )

        for image in range(number_of_images):
            im = Image.objects.create(
                user = user,
                description = "race week",
                photo = "https://i.ibb.co/jRJ5QxW/1a53d3ee1504.jpg",
                location = "monaco"
            )
            im.tags.add("f1","monaco")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('api:searchimage'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('api:searchimage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/search.html')
    
    def test_search_image_by_tag(self):
        number_of_images = 2
        response = self.client.get("/search/?tags=f1")
        image = Image.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['Images']), number_of_images)
        self.assertEqual(len(response.context['tags']), 1)
    

class CollectionDetailViewTest(TestCase):
    def setUp(self):
        number_of_images = 2
        user = User.objects.create(
            username="test_user",
            first_name = "mohamed",
            last_name = "hamaida",
            email = "mohamed@gmail.com",
            password="123456789abc"
            )
        for image in range(number_of_images):
            im = Image.objects.create(
                user = user,
                description = "race week",
                photo = "https://i.ibb.co/jRJ5QxW/1a53d3ee1504.jpg",
                location = "monaco"
            )
            im.tags.add("f1","monaco")
        
        collection = Collection.objects.create(
            name = "my collection",
            private = True,
            user = user
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/colection/1')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('api:collectiondetail',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('api:collectiondetail',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'api/collection_detail.html')

    def test_create_collection_not_loged_in_user(self):
        response = self.client.get(reverse('api:createcollection'))
        url = reverse('account_login')+"?next=/createcollection/"
        self.assertRedirects(response,url)
    
    def test_delete_collection_not_loged_in_user(self):
        response = self.client.get(reverse('api:deletecollection',kwargs={'pk':1}))
        url = reverse('account_login')+"?next=/deletecollection/1"
        self.assertRedirects(response,url)

    def test_add_image_to_collection(self):
        image = Image.objects.first()
        user = User.objects.first()
        collection = Collection.objects.first()
        login = self.client.force_login(user, backend=None)

        response = self.client.get(reverse('api:addimagetocollection',kwargs={'collection_id':1,'image_id':image.id}))
        self.assertRedirects(response,reverse('api:image',kwargs={'pk':image.id}))

    def test_remove_image_from_collection(self):
        image = Image.objects.first()
        user = User.objects.first()
        collection = Collection.objects.first()
        login = self.client.force_login(user, backend=None)

        response = self.client.get(reverse('api:removeimagefromcollection',kwargs={'collection_id':1,'image_id':image.id}))
        self.assertRedirects(response,reverse('api:image',kwargs={'pk':image.id}))


