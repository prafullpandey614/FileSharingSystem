from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', views.ClientUserRegistrationView.as_view(), name='cr'),
    path('api/verify-otp',views.Register.as_view(),name="verify-otp"),
    path('api/generate-otp',views.Register.as_view(),name="register-client-with-otp"),
    path('api/register-operationuser/', views.OperationUserRegistrationView.as_view(), name='opr'),
    path('api/upload-file/', views.UploadFileView.as_view(), name='upload-file'),
    path('api/download/<int:pk>', views.DownloadFileView.as_view(), name='download-file'),
    path('api/down/<int:pk>', views.GetDownloadLinkAPIView.as_view(), name='encryp'),
    path('api/all-files', views.AllFilesView.as_view(), name='encryp'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]