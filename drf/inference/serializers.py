from rest_framework import serializers
from .models import ChestXray, CoughAudio, MultiData

class ChestXraySerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(use_url=True)
    
    class Meta:
        model = ChestXray
        fields = '__all__'
    
    def get_photo_url(self, car):
        request = self.context.get('request')
        photo_url = car.photo.url
        
        return request.build_absolute_uri(photo_url)


class CoughAudioSerializer(serializers.ModelSerializer):
    # mel = serializers.ImageField(use_url=True)
    
    class Meta:
        model = CoughAudio
        fields = '__all__'
    
    # def get_photo_url(self, car):
    #     request = self.context.get('request')
    #     mel_url = car.mel.url
        
    #     return request.build_absolute_uri(mel_url)


class MultiDataSerializer(serializers.ModelSerializer):    
    class Meta:
        model = MultiData
        fields = '__all__'