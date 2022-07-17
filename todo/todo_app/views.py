import pytz
import datetime
from rest_framework.generics import (
    CreateAPIView, 
    GenericAPIView,
    ListAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from passlib.hash import pbkdf2_sha256
from .models import SubTask, Task, ToDoUser
from .serializers import (
        UserSignUpSerializer, 
        UserLoginInSerializer, 
        CreateTaskSerialzer,
        CreateSubTaskSerializer
    )

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
        except:
            return Response({
                "message": f"Something went unwxpected wrong",
                "payload": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateTask(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateTaskSerialzer

    def post(self, request):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)

            if not serializer.is_valid():
                raise Exception('Incorrect data found')

            task = serializer.save()
            
            task_id = task.id
            user_task_id = task.user.id
            task_title = task.title
            return Response({ 
                "message": "success",
                "payload": {
                    "taskId": task_id,
                    "userTaskId": user_task_id,
                    "taskTitle": task_title
                }
            }, status=status.HTTP_201_CREATED)
        except Exception:
            return Response({ 
                "message": "Something went unwxpected wrong",
                "payload": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateSubTask(CreateAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateSubTaskSerializer

    def post(self, request):
        try:
            data = request.data
            serializer = self.get_serializer(data=data)

            if not serializer.is_valid():
                raise Exception('Incorrect data found')

            sub_task = serializer.save()
            
            task_id = sub_task.task.id
            task_title = sub_task.task.title
            sub_task_id = sub_task.id
            sub_task_description = sub_task.description
            sub_task_created_at = sub_task.created_date
            sub_task_remind = sub_task.remind
            sub_task_reminder_datetime = sub_task.reminder_datetime
            
            return Response({
                "message": "success",
                "payload": {
                    "taskId": task_id,
                    "subTaskId": sub_task_id,
                    "taskTitle": task_title,
                    "subtaskDescription": sub_task_description,
                    "subTaskCreatedAt": sub_task_created_at,
                    "remind": sub_task_remind,
                    "reminderDateTime": sub_task_reminder_datetime
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "message": "Something went unexpected wrong",
                "pasyload": {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllTask(ListAPIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            user_id = request.session.get('userId', None)
            
            if not user_id:
                raise Exception('User not found')
            
            task = Task.objects.filter(user__id=user_id).values()

            return Response({
                "message": "success",
                "payload": task
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "message": "Something went unexpected wrong",
                "payload": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetSubTask(ListAPIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        try:
            user_id = request.session.get('userId', None)
            task_id = int(request.GET.get('taskId', '0'))
            
            if not user_id:
                raise Exception('User not found')
            
            sub_task = SubTask.objects.prefetch_related('Task').filter(task__id=task_id).values()

            return Response({
                "message": "success",
                "payload": sub_task
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "message": "Something went unexpected wrong",
                "payload": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateTask(UpdateAPIView):

    def put(self, request):
        try:
            data = request.data
            title_id = data.get('taskId')
            title_to_update = data.get('title')
            user_id = request.session.get('userId', None)

            if not user_id:
                raise Exception('User not in session')
            
            Task.objects.filter(id=title_id, user__id=user_id).update(title=title_to_update)
            
            return Response({
                "message": "success"
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "message": "Something went unexpected wrong"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateSubTask(UpdateAPIView):

    def put(self, request):
        try:
            data = request.data
            sub_task_id = data.get('subTaskId')
            desc_to_update = data.get('desc')
            user_id = request.session.get('userId', None)

            if not user_id:
                raise Exception('User not in session')
            
            SubTask.objects.filter(id=sub_task_id).update(description = desc_to_update)
            
            return Response({
                "message": "success"
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "message": "Something went unexpected wrong"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteTask(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        try:
            task_id = int(kwargs.get('taskId', '0'))
            task = Task.objects.filter(id=task_id)

            if not task.exists():
                raise Exception('Task not found')
            
            task[0].delete()
            return Response({
                'message': "Task deleted successfully"
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'message': "Something went unexpected wrong"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeleteSubTask(DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        try:
            sub_task_id = int(kwargs.get('subTaskId', '0'))
            sub_task = SubTask.objects.filter(id=sub_task_id)

            if not sub_task.exists():
                raise Exception('Task not found')
            
            sub_task[0].delete()
            return Response({
                'message': "Sub-Task deleted successfully"
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'message': "Something went unexpected wrong"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TaskNotification(ListAPIView):
    def get(self, request):
        try:
            response_list = []
            utc = pytz.UTC
            all_sub_task = SubTask.objects.filter(remind=True, is_completed=0).values()
            
            if not all_sub_task.exists():
                return Response({'message': 'No schedule task found'}, status=status.HTTP_204_NO_CONTENT)

            for sub_task in all_sub_task:
                current_utc_date = utc.localize(datetime.datetime.utcnow()).strftime("%m/%d/%Y, %H:%M")
                if sub_task.get('reminder_datetime').strftime("%m/%d/%Y, %H:%M") == current_utc_date:
                    SubTask.objects.filter(id=sub_task.get('id')).update(remind=False)
                    response_list.append(sub_task)

            return Response({
                "payload": response_list
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                "payload": []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)