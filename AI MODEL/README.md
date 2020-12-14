# AI MODEL

<br/>

COVID19 진단에 사용될 모델 구현 

흉부 X-ray 이미지와 기침 소리를 이용해 분류하는 모델 구현


## Audio model

### 1. 데이터 전처리 
a) 필요없는 데이터를 제거한다.
오디오 파일이 비어있거나, 기침소리 외에 다른소리가 녹음되어 있는 경우 파일을 제거한다. 

b) 데이터를 나눈다.
데이터 부족을 보완하기 위하여, 1초 단위로 기침소리를 한번 혹은 두번으로 분할한다. 

c) 데이터 augmentation을 진행한다. 
백색소음을 추가하여 augmentation을 진행한다. (본선 시 오디오 이동, 속도를 빠르기 조절은 데이터 중복 우려로 생략) 

d) WAV 파일 변환 후 저장
WAV 파일을 librosa 라이브러리를 활용하여 mel-spectrogram으로 변환 후 image 파일로 저장한다. 

### 2. 모델 구축
a) Densent 201을 활용하여 features을 추출한 후 저장한다. 
b) COVID 와 NON-COVID 로 binary classifier을 진행한다. 
c) 89%의 정확도 달성

### 3. 예측 
a) WAV 파일을 image 파일로 저장하여 예측하는 code를 구현한다. 

--------------
