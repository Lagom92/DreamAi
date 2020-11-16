from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ChestXraySerializer, CoughAudioSerializer, MultiDataSerializer
from .models import ChestXray, CoughAudio, MultiData
from .apps import InferenceConfig
from inference.myPredicts import make_wav2img, predict_multiInput


@api_view(['GET', 'POST'])
def predictImage(request):
    '''

    CXR image 저장 및 list 조회 API

    ### GET

    - 최신순(order=-id) CXR image list

    ### POST

    - 단일 CXR 이미지 저장

    - POST 요청 시 body에 form-data로 

    | KEY   | VALUE         | DESCRIPTION |
    | ----- | ------------- | ----------- |
    | photo | CXR_image.jpg |             |

    '''
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
    '''

    CXR image detail API

    - pk에 해당하는 CXR image 조회 및 inference 실행

    - prediction이 이미 있는 경우 inference 생략

    '''
    xray = get_object_or_404(ChestXray, pk=pk)
    if xray.prediction == None:
        prediction = InferenceConfig.predict_CXR(xray.photo.path)
        xray.prediction = prediction
        xray.save()

    serializer = ChestXraySerializer(xray, context={"request":request})
    return Response(serializer.data)


@api_view(['GET'])
def newImage(request):
    '''

    CXR image detail API

    가장 최근 저장된 CXR image 조회 및 inference 실행

    - prediction이 이미 있는 경우 inference 생략

    '''
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
    '''

    Cough audio 저장 및 list 조회 API

    ### GET

    - 최신순(order=-id) Cough audio list

    ### POST

    - 단일 Cough 오디오 저장

    - POST 요청 시 body에 form-data로 

    | KEY   | VALUE            | DESCRIPTION |
    | ----- | ---------------- | ----------- |
    | audio | Cough_audio.wav |             |

    '''
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
    '''

    Cough audio detail API

    - pk에 해당하는 Cough audio 조회 및 inference 실행

    - prediction이 이미 있는 경우 inference 생략

    '''
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


@api_view(['GET'])
def newAudio(request):
    '''

    Cough audio detail API

    가장 최근 저장된 Cough audio 조회 및 inference 실행

    - prediction이 이미 있는 경우 inference 생략

    '''
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


@api_view(['GET', 'POST'])
def predictMulti(request):
    '''

    Multi(CXR image and Cough audio) 저장 및 list 조회 API

    ### GET

    - 최신순(order=-id) Multi list

    ### POST

    - Multi 저장

    - POST 요청 시 body에 form-data로 

    | KEY   | VALUE            | DESCRIPTION |
    | ----- | ---------------- | ----------- |
    | photo | CXR_image.jpg    |             |
    | audio | Cough_audio.wav  |             |

    '''
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
    '''

    Multi detail API

    - pk에 해당하는 Multi 조회 및 inference 실행

    - prediction이 이미 있는 경우 inference 생략

    '''
    data = get_object_or_404(MultiData, pk=pk)
    if data.prediction == None:
        audio_mel_path = make_wav2img(data.audio.path)
        prediction = predict_multiInput(data.photo.path, audio_mel_path)
        data.mel = audio_mel_path[8:]
        data.prediction = prediction
        data.save()

    serializer = MultiDataSerializer(data, context={"request":request})
    return Response(serializer.data)


@api_view(['GET'])
def newMulti(request):
    '''

    Multi detail API

    가장 최근 저장된 Multi 조회 및 inference 실행

    - prediction이 이미 있는 경우 inference 생략

    '''
    data = MultiData.objects.last()
    if data.prediction == None:
        audio_mel_path = make_wav2img(data.audio.path)
        prediction = predict_multiInput(data.photo.path, audio_mel_path)
        data.mel = audio_mel_path[8:]
        data.prediction = prediction
        data.save()

    serializer = MultiDataSerializer(data, context={"request":request})
    return Response(serializer.data)
