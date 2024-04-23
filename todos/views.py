from django.shortcuts import render
from rest_framework  import generics, status
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from .serializers import *
from django.http import Http404
from .models import *

# Create your views here.

# class ListTodo(generics.ListAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = ToDoSerializer
# class DetailTodo(generics.RetrieveUpdateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = ToDoSerializer
# class CreateTodo(generics.CreateAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = ToDoSerializer
# class DeleteTodo(generics.DestroyAPIView):
#     queryset = Todo.objects.all()
#     serializer_class = ToDoSerializer

# @api_view(['POST'])
# def registertodo(request):

#     reg = Todo.objects.create(
#         Title = request.data['Title'],
#         Description = request.data['Description'],
#         Date = request.data['Date'],
#         Completed = request.data['Completed'],
#     )
#     serializer = ToDoSerializer(reg, many=True)
#     return Response(serializer.data)

# @api_view(['POST'])
# def updatetodo(request):

#     regs = Todo.objects.update(
#         Title = request.data['Title'],
#         Description = request.data['Description'],
#         Date = request.data['Date'],
#         Completed = request.data['Completed'],
#     )
#     serializer = ToDoSerializer(regs, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def retrive(response, pk):

#     regss = Todo.objects.get(pk=pk)
#     serializer = ToDoSerializer(regss, many=True)
#     return Response(serializer.data)


# @api_view(['GET', 'PUT', 'DELETE'])
# def snippet_detail(request, pk):
#     """
#     Retrieve, update or delete a code snippet.
#     """
#     try:
#         snippet = Snippet.objects.get(pk=pk)
#     except Snippet.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class Updatingtodos(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404

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
