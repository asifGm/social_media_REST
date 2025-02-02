from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import VerificationCode
from .serializers import UserRegistrationSerializer, VerifyEmailSerializer

class RegisterUserView(APIView):
    # Parse and validate user input
    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            if User.objects.filter(username=username).exists():
                return Response({'error': "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Create user with inactive status
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()

        # Generate verification code
            verification_code = get_random_string(length=6, allowed_chars='123456789')
            VerificationCode.objects.create(user=user, code=verification_code)

        # Send verification email
            try:
                send_mail('Your Verification Code', 
                          f"Your code is: {verification_code}", 
                          'noreply@myproject.com', [email], 
                          fail_silently=False
                )
            except Exception as e:
                user.delete()
                return Response({'error': "Failed to send verification email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({'message': "User created. Check your email for the verification code."})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

register_user_view = RegisterUserView.as_view()





class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            code = serializer.validated_data['code']
        

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response({'error': "User does not exist"},  status=status.HTTP_400_BAD_REQUEST)
        

            try:
                verification_record = VerificationCode.objects.get(user=user)
            except VerificationCode.DoesNotExist:
                return Response({'error': "No verification code found for this user"}, status=status.HTTP_400_BAD_REQUEST)
        
        
            if verification_record.code != code:
                return Response({'error': "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)
        
            user.is_active = True
            user.save()

            verification_record.is_verified = True
            verification_record.save()

            return Response({'message': "Email verified successfully! You can now complete your profile."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

verify_email_view = VerifyEmailView.as_view()




