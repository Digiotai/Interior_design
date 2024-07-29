from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", testing, name="testing"),
    path('api', api, name='api'),
    path(r'login', loginpage, name='login'),
    path(r'register', register, name='register'),
    ##path("api/getResult", genAIPrompt, name="GenAIPrompt"),
    path("getImage", genAIPrompt2, name="GenAIPrompt2"),
    path("sendEmail", send_email, name="send_image_email"),
    #path("api/getAnalytics", genAIPrompt3, name="GenAIPrompt3"),
    #path("api/regenerate", regenerate_txt, name="regenerate"),
    #path("api/regenerate_chart", regenerate_chart, name="regenerate_chart"),
    #path("api/genresponse", genresponse, name="answer"),
    path('paymenthandler/', paymenthandler, name='paymenthandler'),
    path('paymentinfo', paymentinfo, name='paymentinfo'),
    path("get_user_details", get_user_details, name="get_user_details"),
    path("updateuserplan", updateuserplan, name="updateuserplan"),
    path("googlelogin", googlelogin, name="googlelogin"),

    path("password_reset",auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_done",auth_views.PasswordResetDoneView.as_view(), name=" password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name=" password_reset_confirm"),
    path("password_reset_complete", auth_views.PasswordResetCompleteView.as_view(), name=" password_reset_complete"),
    path("generateImage", generateImage, name='generateImage'),
    #path("api/generatetestImage", generatetestImage, name='generatetestImage'),
]


