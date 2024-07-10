from django.urls import path
from .views import *

urlpatterns = [
    path("", testing, name="testing"),
    path(r'api/login', loginpage, name='login'),
    path(r'api/register', register, name='register'),
    path("api/upload", upload_data, name="upload_data"),
    path("api/getResult", genAIPrompt, name="GenAIPrompt"),
    path("api/getImage", genAIPrompt2, name="GenAIPrompt2"),
    path("api/getAnalytics", genAIPrompt3, name="GenAIPrompt3"),
    path("api/regenerate", regenerate_txt, name="regenerate"),
    path("api/regenerate_chart", regenerate_chart, name="regenerate_chart"),
    path("api/genresponse", genresponse, name="answer"),
    path('api/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('api/paymentinfo', paymentinfo, name='paymentinfo'),
    path("api/get_user_details", get_user_details, name="get_user_details"),
    path("api/updateuserplan", updateuserplan, name="updateuserplan"),
    path("api/googlelogin", googlelogin, name="googlelogin"),
    path("api/generateImage", generateImage, name='generateImage'),
    path("api/generatetestImage", generatetestImage, name='generatetestImage'),
]
