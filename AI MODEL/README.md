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
백색소음을 추가하여 augmentation을 진행한다. <br>
(본선 시 오디오 이동, 속도를 빠르기 조절은 데이터 중복 우려로 생략) 

d) WAV 파일 변환 후 저장
WAV 파일을 librosa 라이브러리를 활용하여 mel-spectrogram으로 변환 후 image 파일로 저장한다. 

### 2. 모델 구축
a) Densent 201을 활용하여 features을 추출한 후 저장한다. 

b) COVID 와 NON-COVID 로 binary classification을 진행한다. 

c) 89%의 정확도 달성

### 3. 예측 
a) WAV 파일을 image 파일로 저장하여 예측하는 code를 구현한다. 

--------------

## Image model

### 1. 데이터 전처리
a) Chest X-ray 이미지를 segmentation하여 폐의 위치를 대략적으로 찾는다. <br>
(폐만 따로 추출하지 않은 이유는 segmentation모델의 성능을 100% 신뢰할 수 없기 때문으로, 잘못 분할할 시 폐에 대한 정보를 소실할 우려가 있음.)

b) 흑백으로 분할된 이미지를 사용하여 폐를 둘러싸는 bounding box를 생성한다.(빨간색)

c) 폐를 감싸는 절반의 패딩을 준 bounding box를 형성한다.(파란색)

d) 최종적으로 CXR이미지에서 폐가 확대된 이미지를 얻는다. ( 폐와 관련되지 않은 데이터 제거 )

### 2. 모델 구축
a) Densent 201을 활용하여 features을 추출한 후 저장한다. 

b) COVID 와 NON-COVID 로 binary classification을 진행한다. 

c) 99%의 정확도 달성 (이미지 단일 분류 모델)

### 3. 예측
a) 전처리된 CXR이미지를 분류기에 통과시켜 COVID를 예측한다.

--------------------

## multi model
오디오와 이미지 분류모델을 융합한 모델로 covid-19를 좀 더 효과적으로 분류할 수 있는 방법을 모색하기 위한 모델.

### 1. 데이터 전처리

a) 오디오 모델과 이미지 모델의 전처리 방법을 각각 수행한다.

b) 오디오 데이터와 이미지 데이터 둘 모두 이미지의 형태로 전처리가 완료된다.

### 2. 모델 구축
a) 전체적인 구조는 다중입력 분류모델로, 입력으로는 오디오 전처리에서 만들어진 이미지와 이미지 전처리를 통해 만들어진 이미지가 들어간다. <br>
(이 과정에서 새로운 데이터로더를 구축하고 학습 시 차례로 데이터를 로드하여 메모리 과부하 현상을 억제한다.)

c) 입력으로 들어온 두 종류의 이미지를 각각 Densenet201 특징추출 모델을 사용하여 특징 추출한다.

d) 추출된 두 종류의 특징을 병합(concatenation)한다.

e) 병합된 특징으로 분류기를 학습시킨다.

### 3. 예측
오디오 wav파일과 CXR 이미지를 전처리하여 모델에 입력으로 넣어주면 환자의 두 종류의 데이터를 통해 covid19를 예측할 수 있다.
