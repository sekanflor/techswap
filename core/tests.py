# tests.py placeholder

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile, Listing, SwapRequest

class UserProfileTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.user_profile = UserProfile.objects.create(user=self.user, bio='Test bio', location='Test location')

    def test_list_user_profiles(self):
        response = self.client.get('/api/user-profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_profile(self):
        data = {'user': self.user.id, 'bio': 'New bio', 'location': 'New location'}
        response = self.client.post('/api/user-profiles/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user_profile(self):
        response = self.client.get(f'/api/user-profiles/{self.user_profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_profile(self):
        data = {'bio': 'Updated bio', 'location': 'Updated location'}
        response = self.client.put(f'/api/user-profiles/{self.user_profile.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_profile(self):
        response = self.client.delete(f'/api/user-profiles/{self.user_profile.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ListingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.listing = Listing.objects.create(owner=self.user, title='Test Listing', description='Test description', category='Test category')

    def test_list_listings(self):
        response = self.client.get('/api/listings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_listing(self):
        data = {'owner': self.user.id, 'title': 'New Listing', 'description': 'New description', 'category': 'New category'}
        response = self.client.post('/api/listings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_listing(self):
        response = self.client.get(f'/api/listings/{self.listing.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_listing(self):
        data = {'title': 'Updated Listing', 'description': 'Updated description', 'category': 'Updated category'}
        response = self.client.put(f'/api/listings/{self.listing.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_listing(self):
        response = self.client.delete(f'/api/listings/{self.listing.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class SwapRequestTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.listing = Listing.objects.create(owner=self.user, title='Test Listing', description='Test description', category='Test category')
        self.swap_request = SwapRequest.objects.create(listing=self.listing, requester=self.user, status='Pending', message='Test message')

    def test_list_swap_requests(self):
        response = self.client.get('/api/swap-requests/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_swap_request(self):
        data = {'listing': self.listing.id, 'requester': self.user.id, 'status': 'Pending', 'message': 'New message'}
        response = self.client.post('/api/swap-requests/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_swap_request(self):
        response = self.client.get(f'/api/swap-requests/{self.swap_request.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_swap_request(self):
        data = {'status': 'Approved', 'message': 'Updated message'}
        response = self.client.put(f'/api/swap-requests/{self.swap_request.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_swap_request(self):
        response = self.client.delete(f'/api/swap-requests/{self.swap_request.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
