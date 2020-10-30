from django.shortcuts import render, get_object_or_404
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .models import ChestXray
from .serializers import ChestXraySerializer
from .ml.predict import predict_CXR


@api_view(['GET', 'POST'])
# @permission_classes((IsAuthenticated, ))
# @authentication_classes((JSONWebTokenAuthentication, ))
def predictImage(request):
    if request.method == 'GET':
        queryset = ChestXray.objects.all().order_by('-id')
        serializer = ChestXraySerializer(queryset, context={"request":request}, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChestXraySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def detail(request, pk):
    xray = get_object_or_404(ChestXray, pk=pk)
    if xray.prediction == None:
        prediction = predict_CXR(xray.photo.path)
        xray.prediction = prediction
        xray.save()

    if request.method == 'GET':
        serializer = ChestXraySerializer(xray, context={"request":request})
        return Response(serializer.data)

