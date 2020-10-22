from django.shortcuts import render, get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import ChestXray
from .serializers import ChestXraySerializer


@api_view(['GET', 'POST'])
def predictImage(request):
    if request.method == 'GET':
        queryset = ChestXray.objects.all()
        serializer = ChestXraySerializer(queryset, context={"request":request}, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChestXraySerializer(data=request.data)
        # print(serializer.data)
        if serializer.is_valid():
            serializer.save()

            # Image prediction
            print(serializer)
            print(serializer.validated_data)
            serializer.validated_data['prediction'] = "test"
            serializer.save()


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def detail(request, pk):
    xray = get_object_or_404(ChestXray, pk=pk)
    print(xray)

    if request.method == 'GET':
        serializer = ChestXraySerializer(xray, context={"request":request})
        return Response(serializer.data)

