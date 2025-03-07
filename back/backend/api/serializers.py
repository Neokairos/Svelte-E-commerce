from rest_framework import serializers, exceptions
from .models import Product
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User
from .utils import validate_email as email_is_valid


class RegistrationSerializer(serializers.ModelSerializer[User]):
    
    password = serializers.CharField(max_length=20,min_length=1,write_only=True)
    tokens = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['username',
                'email',
                'password',
                'is_staff',
                'is_active',
                'created_at',
                'updated_at',
                'birth_date',
                'tokens']

    def validate_email(self, value:str) -> str:
        valid, error_text = email_is_valid(value)
        if not valid:
        #if valid is False
            raise serializers.ValidationError(error_text)
        try:
            #splitting the email in two vars and starting it from @
            email_name, domain_part = value.strip().rsplit('@',1)
        except ValueError:
            raise ValueError("Email address must contain exactly one '@' symbol.")
        else:
            value = '@'.join([email_name, domain_part.lower()])
            
        return value
            


    def get_tokens(self, obj):
        #obj is the user instance being serialized
        user = User.objects.get(email=obj.email)
        
        return {'refresh': user.tokens['refresh']}
    

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], email=validated_data['email'], password=validated_data['password']
        )
        return user

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')

    class Meta:
        model = Product
        fields = ['id','seller', 'title', 'price', 'description', 'image', 'rating']
    def create(self, validated_data):
        image = validated_data.pop('image')
        product = Product.objects.create(**validated_data)
        product.image.save(image.name, image)
        return product

class LoginSerializer(serializers.ModelSerializer[User]):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        #obj is the user instance being serialized
        user = User.objects.get(email=obj.email)
        
        return {'refresh': user.tokens['refresh'], 'access': user.tokens['access']}
    
    class Meta:
        model = User
        fields = ['email', 'username','password', 'tokens']
        
    def validate(self,data):
        #validating and return user login
        email = data.get('email',None)
        password = data.get('password',None)
        if email is None:
            raise serializers.ValidationError('An email address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = authenticate(username=email, password=password)
        
        if user is None:
            raise serializers.ValidationError('A user with this email and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user is not currently activated.')

        return user
    
class UserSerializer(serializers.ModelSerializer[User]):
        """Handle serialization and update of User objects."""
      
        password = serializers.CharField(max_length=128, min_length=1, write_only=True)

        class Meta:
            model = User
            fields = (
                'id',
                'email',
                'username',
                'password',
                'tokens',
                'birth_date',
                'is_staff',
            )
            read_only_fields = ('tokens', 'is_staff')
            
        def update(self, instance, validated_data):
            password = validated_data.pop('password', None)
            
            for (key, value) in validated_data.items():
                setattr(instance, key, value)
            if password is not None:
                instance.set_password(password)
            
            instance.save()
            
            return instance
        
class LogoutSerializer(serializers.Serializer[User]):
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    def save(self, **kwargs):  
        """Validate save backlisted token."""

        try:
            RefreshToken(self.token).blacklist()

        except TokenError as ex:
            raise exceptions.AuthenticationFailed(ex)
        