from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", testing, name="testing"),
    path('api', api, name='api'),
    path(r'api/login', loginpage, name='login'),
    path(r'api/register', register, name='register'),
    ##path("api/getResult", genAIPrompt, name="GenAIPrompt"),
    path("api/getImage", genAIPrompt2, name="GenAIPrompt2"),
    path("api/sendEmail", send_email, name="send_image_email"),
    #path("api/getAnalytics", genAIPrompt3, name="GenAIPrompt3"),
    #path("api/regenerate", regenerate_txt, name="regenerate"),
    #path("api/regenerate_chart", regenerate_chart, name="regenerate_chart"),
    #path("api/genresponse", genresponse, name="answer"),
    path('api/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('api/paymentinfo', paymentinfo, name='paymentinfo'),
    path("api/get_user_details", get_user_details, name="get_user_details"),
    path("api/updateuserplan", updateuserplan, name="updateuserplan"),
    path("api/googlelogin", googlelogin, name="googlelogin"),

    path("api/password_reset",auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("api/password_reset_done",auth_views.PasswordResetDoneView.as_view(), name=" password_reset_done"),
    path("api/password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name=" password_reset_confirm"),
    path("api/password_reset_complete", auth_views.PasswordResetCompleteView.as_view(), name=" password_reset_complete"),
    path("api/generateImage", generateImage, name='generateImage'),
    #path("api/generatetestImage", generatetestImage, name='generatetestImage'),
]


