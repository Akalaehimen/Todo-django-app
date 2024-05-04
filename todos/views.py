from django.shortcuts import render
from rest_framework  import generics, status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from django.http import Http404
from .models import *
 


# class Updatingtodos(APIView):
#     permission_classes = [IsAuthenticated]
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, pk):
#         try:
#         # Ensure that the todo belongs to the authenticated user
#             user_instance = self.request.user
#             if isinstance(user_instance, User):
#                return Todo.objects.get(pk=pk, user=user_instance)
#             else:
#                raise Http404("User not found")
#         except Todo.DoesNotExist:
#             raise Http404("Todo not found")


    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ToDoSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ToDoSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Creatingandgetting(APIView):
    permission_classes = (IsAuthenticated,)
    """
    Creating or getting the whole todos.
    """
    def get_object(self):
        try:
            return Todo.objects.all()
        except Todo.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = self.get_object()  # Use get_object() to fetch queryset15
        serializer = ToDoSerializer(snippets, many=True)  # Use many=True for queryset
        return Response(serializer.data)

    def post(self, request, format=None):
        
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_201_CREATED)
