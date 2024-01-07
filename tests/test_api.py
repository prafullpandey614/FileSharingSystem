import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
@pytest.mark.django_db
class TestGetDownloadLinkAPIView:
    def setup_method(self, method):
        self.client = APIClient()

    def test_get_download_link(self):

        response = self.client.get(path="/api/down/1")

        assert response.status_code == status.HTTP_200_OK
        assert 'api/download/1' in response.data

    def test_get_download_link_invalid_pk(self):

        response = self.client.get(path="/api/down/930")

        assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
class TestOperationUser:
    def setup_method(self, method):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',email="tese@gmail.com", password='testpassword')
        self.client.force_authenticate(user=self.user)
    def test_op_user(self):

        response = self.client.post(path="/api/token/",data={"username" :"testuser","Password":"testpassword"})

        assert response.status_code == status.HTTP_200_OK


    def test_get_download_link_invalid_pk(self):

        response = self.client.get(path="/api/down/10231")

        assert response.status_code == status.HTTP_404_NOT_FOUND
