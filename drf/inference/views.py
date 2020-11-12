from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChestXraySerializer, CoughAudioSerializer, MultiDataSerializer
from .models import ChestXray, CoughAudio, MultiData
from .apps import InferenceConfig
from inference.multi_pred import make_wav2img, predict_multiInput
import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import librosa
import os


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


@api_view(['GET'])
def detail(request, pk):
    xray = get_object_or_404(ChestXray, pk=pk)
    if xray.prediction == None:
        prediction = InferenceConfig.predict_CXR(xray.photo.path)
        xray.prediction = prediction
        xray.save()

    if request.method == 'GET':
        serializer = ChestXraySerializer(xray, context={"request":request})
        return Response(serializer.data)


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


@api_view(['GET'])
def detailAudio(request, pk):
    cough = get_object_or_404(CoughAudio, pk=pk)
    audio_path = cough.audio.path
    y, sr = librosa.load(audio_path, sr = None)
    S = librosa.feature.melspectrogram(y, sr=22050, n_mels=128) 
    S_DB = librosa.power_to_db(S, ref=np.max)
    img = librosa.display.specshow(S_DB, sr=22050)
    title = audio_path.split('\\')[-1][:-4]
    image_path = './media/mel/'+ title +'.jpg'
    if not os.path.isdir('./media/mel'):
        os.mkdir('./media/mel')
    plt.savefig(image_path)
    prediction = InferenceConfig.predict_audio(image_path)
    cough.mel = image_path[8:]
    cough.prediction = prediction
    cough.save()

    context = {
        "id": cough.id,
        "audio": "/media/" + str(cough.audio),
        "mel": "/media/" + str(cough.mel),
        "created_at": cough.created_at,
        "prediction": cough.prediction,
    }

    return Response(context)


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