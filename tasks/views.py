from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from bson.objectid import ObjectId
from rest_framework.views import APIView

# MongoDB Operation imports
from .mongo_operations import (insert_item,
                               get_items,
                               find_one,
                               update_item,
                               delete_one, )

# For Authentication
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token


class TaskViewListSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        print("Inside list")
        paginator = PageNumberPagination()
        paginator.page_size = 3
        user_id = request.user.id
        tasks = list(
            get_items(user_id=user_id)
        )
        paginated_tasks = paginator.paginate_queryset(list(tasks), request=request)

        for task in paginated_tasks:
            task['_id'] = str(task['_id'])

        return paginator.get_paginated_response(paginated_tasks)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user_name = request.data.get('username')

        if email and password and user_name:
            user = User.objects.create_user(email=email, password=password, username=user_name)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {'token': token.key},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'All Required fields not present'},
                status=status.HTTP_400_BAD_REQUEST
            )


class TaskViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Inside post")
        data = request.data
        user_id = request.user.id

        task = insert_item(user_id=user_id, data=data)
        task_id = task.inserted_id
        return Response(
            {'_id': str(task_id)},
            status=status.HTTP_201_CREATED
        )

    def get(self, request):
        pk = None
        print("Inside get")
        user_id = request.user.id
        task = find_one(user_id=user_id, id=request.query_params.get('id'))

        if task:
            task['_id'] = str(task['_id'])
            return Response(task)

        return Response(
            {'Failure': 'No object found'},
            status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request):
        print("Inside put")
        data = request.data
        user_id = request.user.id
        pk = data.get('id')

        result = update_item(user_id=user_id, id=pk, item_data=data)

        if result.matched_count:
            return Response(
                {'Success': 'Updated successfully'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'Failure': 'No matched item found to update'},
            status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request):
        print("Inside delete")
        user_id = request.user.id
        result = delete_one(user_id=user_id, id=request.query_params.get('id'))

        if result.deleted_count:
            return Response(
                {'Success': 'deleted object successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'Failure': 'Object not found'},
            status=status.HTTP_404_NOT_FOUND
        )
