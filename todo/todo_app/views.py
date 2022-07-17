from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from passlib.hash import pbkdf2_sha256
from .models import ToDoUser
from .serializers import UserSignUpSerializer, UserLoginInSerializer

class UserSignUp(CreateAPIView):
    '''
        Save the given user detail into db.
        Input: user - name, email & password
        output: user object if found else empty object
    '''
    authentication_classes = []
    permission_classes = []
    serializer_class = UserSignUpSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)

            if not serializer.is_valid():
                raise Exception("Incorrect data found")

            serializer.save()
            user = ToDoUser.objects.get(email=data.get('email'))
            user_id = user.pk
            user_name = user.name
            user_email = user.email

            request.session['userId'] = user_id
            request.session['userName'] = user_name
            request.session['userEmail'] = user_email

            return Response({
                'message': 'sucess',
                "payload": {
                    "userId": user_id,
                    "userName": user_name,
                    "userEmail": user_email
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'message': f'Error in try block - {e}',
                'payload': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserLoginIn(GenericAPIView):
    '''
        Filter the given email with the db, if found return user obj
        else incorrect user
        Input: user - email & password
        Output: user object if found else empty object
    '''
    authentication_classess = []
    permission_classes = []
    serializer_class = UserLoginInSerializer

    def post(self, request):
        try:
            data = request.data
            email = data.get('email', '')
            password = data.get('password', 'null')

            serializer = self.get_serializer(data=data)

            if not serializer.is_valid():
                raise Exception('Email/Password not found')

            user = ToDoUser.objects.filter(email=email)
            if not user.exists():
                raise Exception('Incorrect Email')

            user = user.first()                
            user_id = user.pk
            user_name = user.name
            user_email = user.email
            user_password = user.password

            is_password_match = pbkdf2_sha256.verify(password, user_password)
            
            if not is_password_match:
                raise Exception('Incorrect Password')

            request.session['userId'] = user_id
            request.session['userName'] = user_name
            request.session['userEmail'] = user_email

            return Response({
                "message": "success",
                "payload": {
                    "userId": user_id,
                    "userName": user_name,
                    "userEmail": user_email
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": f"Error in try block - {e}",
                "payload": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateTask(CreateAPIView):
    pass