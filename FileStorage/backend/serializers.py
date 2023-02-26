from rest_framework import serializers
from .models import Image, CustomUser

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id','image','user','encrypted_session_key')
        read_only_fields = ('id',)
        write_only_fields = ('user','encrypted_session_key',)

    def create(self, validated_data):
        user = None
        image_data = validated_data['image']
        encrypted_session_key = validated_data['encrypted_session_key']
        # request = self.context.get("request")
        # if request and hasattr(request, "user"):
        #     user = request.user
        #     print('req has user')
        user =  self.context['request'].user
        
        image = Image.objects.create(user=user, image=image_data, encrypted_session_key=encrypted_session_key)

        return image

class UserSerializer(serializers.ModelSerializer):
    signature = serializers.SerializerMethodField()
    
    def get_signature(self, obj):
        return (obj)
    
    class Meta:
        model = CustomUser
        fields = ('id','username','password','public_key','n', 'signature')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        # images_data = validated_data.pop('images')

        user = CustomUser.objects.create(
            username=validated_data['username'],
            public_key=validated_data['public_key'],
            n=validated_data['n']
        )
        user.set_password(validated_data['password'])
        user.save()

        # for image_data in images_data:
        #     Image.objects.create(user = user, **image_data)
        return user

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','username','public_key','n')



