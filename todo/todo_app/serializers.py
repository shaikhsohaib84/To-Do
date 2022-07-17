from importlib.metadata import requires
from urllib import request
from rest_framework import serializers
from passlib.hash import pbkdf2_sha256
from .models import SubTask, Task, ToDoUser

class UserSignUpSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = ToDoUser.objects.create(
            name = validated_data.get('name'),
            email = validated_data.get('email'),
            password = pbkdf2_sha256.hash(validated_data.get('password')),
        )
        return user
    
    class Meta:
        model = ToDoUser
        fields = '__all__'

class UserLoginInSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = ToDoUser
        fields = ['email', 'password']

class CreateTaskSerialzer(serializers.ModelSerializer):
    taskTitle = serializers.CharField(required=True)
    userId = serializers.IntegerField(required=True)

    def create(self, validated_data):
        user_id = validated_data.get('userId')
        task_title = validated_data.get('taskTitle')
        user = ToDoUser.objects.get(id=user_id)
        user_task_title = Task.objects.create(title=task_title, user=user)
        return user_task_title
    class Meta:
        model = Task
        fields = ['taskTitle', 'userId']

class CreateSubTaskSerializer(serializers.ModelSerializer):
    taskDescription = serializers.CharField(required=True)
    taskId = serializers.CharField(required=True)
    remind = serializers.BooleanField()
    reminder_datetime = serializers.DateTimeField()


    def create(self, validated_data):
        task_id = int(validated_data.get('taskId', '0'))
        task_description = validated_data.get('taskDescription')
        remind = validated_data.get('remind', 0)
        reminder_datetime = validated_data.get('reminder_datetime', None)

        task = Task.objects.get(id=task_id)
        sub_task = SubTask.objects.create(description=task_description, task=task, remind=remind, reminder_datetime=reminder_datetime)
        return sub_task
    class Meta:
        model = SubTask
        fields = ['taskId', 'taskDescription', 'remind', 'reminder_datetime']