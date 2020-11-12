from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChestXraySerializer, CoughAudioSerializer, MultiDataSerializer
from .models import ChestXray, CoughAudio, MultiData
from .apps import InferenceConfig
from inference.myPredicts import make_wav2img, predict_multiInput


'''
CXR
list 및 이미지 저장
'''
@api_view(['GET', 'POST'])
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


'''
CXR
detail 및 inference
'''
@api_view(['GET'])
def detail(request, pk):
    xray = get_object_or_404(ChestXray, pk=pk)
    if xray.prediction == None:
        prediction = InferenceConfig.predict_CXR(xray.photo.path)
        xray.prediction = prediction
        xray.save()

    serializer = ChestXraySerializer(xray, context={"request":request})
    return Response(serializer.data)


'''
CXR
가장 최근 저장된 이미지 불러오기 및 inference
'''
@api_view(['GET'])
def newImage(request):
    xray = ChestXray.objects.last()
    if xray.prediction == None:
        prediction = InferenceConfig.predict_CXR(xray.photo.path)
        xray.prediction = prediction
        xray.save()

    serializer = ChestXraySerializer(xray, context={"request":request})
    return Response(serializer.data)


'''
Cough
list 및 음성 저장
'''
@api_view(['GET', 'POST'])
def predictAudio(request):
    if request.method == 'GET':
        queryset = CoughAudio.objects.all().order_by('-id')
        serializer = CoughAudioSerializer(queryset, context={"request":request}, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CoughAudioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


'''
Cough
detail 및 inference
'''
@api_view(['GET'])
def detailAudio(request, pk):
    cough = get_object_or_404(CoughAudio, pk=pk)
    if cough.prediction == None:
        audio_path = cough.audio.path
        image_path = make_wav2img(audio_path)
        prediction = InferenceConfig.predict_audio(image_path)
        cough.prediction = prediction
        cough.mel = image_path[8:]
        cough.save()

    serializer = CoughAudioSerializer(cough, context={"request":request})
    return Response(serializer.data)


'''
Cough
가장 최근 저장된 음성 불러오기 및 inference
'''
@api_view(['GET'])
def newAudio(request):
    cough = CoughAudio.objects.last()
    if cough.prediction == None:
        audio_path = cough.audio.path
        image_path = make_wav2img(audio_path)
        prediction = InferenceConfig.predict_audio(image_path)
        cough.prediction = prediction
        cough.mel = image_path[8:]
        cough.save()

    serializer = CoughAudioSerializer(cough, context={"request":request})
    return Response(serializer.data)


'''
Multi
list 및 음성 저장
'''
@api_view(['GET', 'POST'])
def predictMulti(request):
    if request.method == 'GET':
        queryset = MultiData.objects.all().order_by('-id')
        serializer = MultiDataSerializer(queryset, context={"request":request}, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = MultiDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


'''
Multi
detail 및 inference
'''
@api_view(['GET'])
def detailMulti(request, pk):
    data = get_object_or_404(MultiData, pk=pk)
    if data.prediction == None:
        audio_mel_path = make_wav2img(data.audio.path)
        prediction = predict_multiInput(data.photo.path, audio_mel_path)
        data.mel = audio_mel_path[8:]
        data.prediction = prediction
        data.save()

    serializer = MultiDataSerializer(data, context={"request":request})
    return Response(serializer.data)


'''
Multi
가장 최근 저장된 이미지, 음성 불러오기 및 inference
'''
@api_view(['GET'])
def newMulti(request):
    data = MultiData.objects.last()
    if data.prediction == None:
        audio_mel_path = make_wav2img(data.audio.path)
        prediction = predict_multiInput(data.photo.path, audio_mel_path)
        data.mel = audio_mel_path[8:]
        data.prediction = prediction
        data.save()

    serializer = MultiDataSerializer(data, context={"request":request})
    return Response(serializer.data)

