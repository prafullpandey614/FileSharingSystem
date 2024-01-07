import mimetypes
# from random import random
import random
from rest_framework import generics,views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse

from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404

from api.models import ClientUser, FileSystem, NewUserOtp, OperationUser
from .utils import send_otp_email

from .serializers import FileSystemSerl, OperationUserSerializer, ClientUserSerializer, UserSerializers

class OperationUserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializers
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        

        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email'],
            is_superuser = True
        )

        client,cre=  OperationUser.objects.get_or_create(user = user)
        client.status = True 
        client.save()


        refresh = RefreshToken.for_user(user) #getting a JWT Token for Authentication
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(token, status=status.HTTP_201_CREATED)



class ClientUserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializers
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create a superuser
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email']
        )

        client,cre=  ClientUser.objects.get_or_create(user = user)
        client.status = True 
        client.save()

        refresh = RefreshToken.for_user(user)
        token = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(token, status=status.HTTP_201_CREATED)

class Register(views.APIView):
    def post(self,request,*args, **kwargs):
        if request.path == "/api/verify-otp":
            otp = request.data["otp"]
            email = request.data["email"]
            
            otp_obj =  NewUserOtp.objects.get(email=email)
            print(otp,"    ",otp_obj.otp)
            if otp_obj.otp == int(otp ):
                user = User.objects.create_user(
                            username=request.data['username'],
                            password=request.data['password'],
                            email=request.data['email']
                        )
                client,cre=  ClientUser.objects.get_or_create(user = user)
                client.status = True 
                client.save()

                refresh = RefreshToken.for_user(user)
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return Response(token, status=status.HTTP_201_CREATED)
                
            else :
                return Response({"Error" : "Please Enter Correct OTP"},400)

            
        if request.path == "/api/generate-otp":
            email = request.data["email"]
            otp = random.randint(1000,9999)
            try : 
                NewUserOtp.objects.get(email=email).delete()
            except :
                pass

            obj = NewUserOtp.objects.create(email=email,otp=otp)
            send_otp_email(email,otp)
            return Response({"otp": obj.otp},200)
        return Response({"message" : " Done"},200)
    
class UploadFileView(generics.CreateAPIView):
    serializer_class = FileSystemSerl
    permission_classes = [IsAuthenticated]

    
    def create(self,request,*args,**kwargs):
        data = request.data 
        data["uploaded_by"] = request.user.id
        
        if not request.user.is_superuser:
            return Response({"Error : Only Operation Users are allowed to Upload Files"},400)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Success : Only Operation Users are allowed to Upload Files"},200)


class GetDownloadLinkAPIView(views.APIView):
    def get(self,request,pk,*args, **kwargs):
        obj  = get_object_or_404(FileSystem,id=pk)
        url_file = request.build_absolute_uri('/')+"api/download/"+str(pk)
        return Response(url_file)

class DownloadFileView(generics.RetrieveAPIView):
    queryset = FileSystem.objects.all()
    serializer_class = FileSystemSerl
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user.id
        # obj = get_object_or_404(ClientUser,user=user) #Now only client users can download
        instance = self.get_object()
        file_path = instance.file.path
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{instance.file.name}"'
        return response

class AllFilesView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,*args, **kwargs):
        data = FileSystem.objects.all()
        data = FileSystemSerl(data,many=True)
        return Response(data.data,200)
    