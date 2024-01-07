import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
@pytest.mark.django_db
class TestGetDownloadLinkAPIView:
    def setup_method(self, method):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email="tese@gmail.com", password='testpassword')
        
    def test_get_download_link(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(path="/api/all-files")


        assert response.status_code == status.HTTP_200_OK
    def test_get_download_un_authorised(self):
    
        response = self.client.get(path="/api/all-files")


        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    def test_get_download_wrong_method(self):
        
        response = self.client.get(path="/api/all-files")


        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    def test_get_download_link_invalid_pk(self):

        response = self.client.get(path="/api/down/930")

        assert response.status_code == status.HTTP_404_NOT_FOUND


