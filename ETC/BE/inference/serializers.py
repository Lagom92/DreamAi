from rest_framework import serializers
from .models import ChestXray, CoughAudio, MultiData

class ChestXraySerializer(serializers.ModelSerializer):    
    class Meta:
        model = ChestXray
        fields = '__all__'


class CoughAudioSerializer(serializers.ModelSerializer):    
    class Meta:
        model = CoughAudio
        fields = '__all__'


class MultiDataSerializer(serializers.ModelSerializer):    
    class Meta:
        model = MultiData
        fields = '__all__'