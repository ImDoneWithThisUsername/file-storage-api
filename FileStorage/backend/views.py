
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import CustomUser, Image
from .serializers import ImageSerializer, UserSerializer, UserInfoSerializer

from .encryption.Encryption import validate_sig

from django.http import HttpResponse

class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request, format=None):
        signature = request.data['signature']
        serializers = UserSerializer(data=request.data)
        
        if serializers.is_valid():
            username = serializers.validated_data['username']
            public_key = serializers.validated_data['public_key']
            n = serializers.validated_data['n']

            if not validate_sig(sig=int(signature),data=username,pub_key=int(public_key),n=int(n)):
                return Response([],status=status.HTTP_400_BAD_REQUEST)
            serializers.save()
            return Response([],status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

class UserImagesView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser,)

    # get list image
    def get(self, request, format=None):
        images = Image.objects.filter(user=request.user)
        if not len(images):
            return Response([], status=status.HTTP_200_OK)
        serializer = ImageSerializer(images, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    # upload image
    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserInfoSerializer

# download image
class DownloadImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, format=None):
        images = Image.objects.filter(pk = pk, user=request.user)
        if not images:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializers = ImageSerializer(images, many=True )
        return HttpResponse(images[0].image, status=status.HTTP_302_FOUND)
    
class ShareImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # target user id, request user img id
    def get(self, request ,format=None):
        target_username = request.query_params.get('target_username')

        user = CustomUser.objects.filter(username=target_username)

        if(len(user)):
            target_pub_key = user[0].public_key
            target_user_n = user[0].n
            payload = {
                "target_pub_key": target_pub_key,
                "target_user_n": target_user_n
            }
            return Response(payload, status=status.HTTP_302_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        re_encrypted_key = request.data['re_encrypted_key']
        img_id = request.data['img_id']
        target_username = request.data['target_username']


        user = CustomUser.objects.filter(username=target_username)
        img_obj = Image.objects.filter(id=img_id, user=request.user)
        
        if(len(user) and len(img_obj)):
            shared = Image.objects.create(
                image=img_obj[0].image,
                user=user[0],
                encrypted_session_key=re_encrypted_key
            )
            serializer = ImageSerializer(shared)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)
