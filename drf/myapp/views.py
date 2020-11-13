from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import serializers
from .serializers import BoardSerializer
from .models import Board

# Create your views here.
class BoardView(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()