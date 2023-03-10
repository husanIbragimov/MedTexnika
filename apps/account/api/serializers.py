from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from apps.account.models import Account
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=68, write_only=True)

    class Meta:
        model = Account
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',
                  'password2'
                  )

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'success': False,
                                               'message': 'Password did not match, please try again'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=101, required=True)
    password = serializers.CharField(max_length=68, write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.CharField(max_length=100, read_only=True)
    last_name = serializers.CharField(max_length=100, read_only=True)
    username = serializers.CharField(max_length=100, read_only=True)

    def get_token(self, obj):
        email = obj.get('email')
        token = Account.objects.get(email=email).token
        return token

    def get_fisrt_name(self, obj):
        user = Account.objects.filter(email=obj.get('email')).first()
        return user.first_name

    def get_last_name(self, obj):
        user = Account.objects.filter(email=obj.get('email')).first()
        return user.last_name

    def get_username(self, obj):
        user = Account.objects.filter(email=obj.get('email')).first()
        return user.username

    class Meta:
        model = Account
        fields = ('id', 'email', 'password', 'token', 'first_name', 'last_name', 'username')

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed({
                "status": False,
                "message": "Email or password is not correct"
            })
        if not user.is_active:
            raise AuthenticationFailed({
                "status": False,
                "message": "Account disabled"
            })

        data = {
            'success': True,
            'id': user.id,
            'email': user.email,
            'tokens': user.token,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }
        return data


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = Account
        fields = ('token',)


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Account
        fields = ('email',)


class SetNewPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)
    uidb64 = serializers.CharField(max_length=68, required=True)
    token = serializers.CharField(max_length=555, required=True)

    class Meta:
        model = Account
        fields = ('password', 'password2', 'uidb64', 'token')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        _id = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.filter(id=_id).first()
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed({'success': False, 'message': 'The token is not valid'})
        if password != password2:
            raise serializers.ValidationError({
                'success': False, 'message': 'Password did not match, please try again'
            })
        user.set_password(password)
        user.save()
        return user


class ChangeNewPasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password = serializers.CharField(min_length=6, max_length=64, write_only=True)
    password2 = serializers.CharField(min_length=6, max_length=64, write_only=True)

    class Meta:
        model = Account
        fields = ('old_password', 'password' 'password2')

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        password = attrs.get('password')
        password2 = attrs.get('password2')
        request = self.context.get('request')
        user = request.user
        if not user.check_password(old_password):
            raise serializers.ValidationError({
                'success': False, 'message': 'Old password did not match, please try again'
            })
        if password != password2:
            raise serializers.ValidationError({
                'success': False, 'message': 'Password did not match, please try again'
            })
        user.set_password(password)
        user.save()
        return attrs


class AccountSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')

    class Meta:
        model = Account
        fields = (
            'id', 'email', 'first_name', 'last_name', 'username',
            'bio',
            'gender',
            'image',
            'is_active',
            'date_login'
        )
