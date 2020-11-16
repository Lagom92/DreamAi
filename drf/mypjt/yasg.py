from django.conf.urls import url
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from drf_yasg import openapi

schema_url_patterns = [
    path('infer/', include('inference.urls')),
]
 
schema_view = get_schema_view(
    openapi.Info(
        title="Febreath Open API",
        default_version='v1',
        description = 
        '''
        <br/>

        Chest X-ray image와 Cough audio를 통해 COVID19를 진단하는 서비스

        <hr/>
        
        TEAM: 폐브리즈(Febreath) 

        양시영, 김진혁, 김주연, 이상훈, 정진균

        ''',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="jyyt0147@gmail.com"),
        license=openapi.License(name="Febreath"),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)