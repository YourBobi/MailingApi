from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import ClientViewSet, MailingViewSet, MessageViewSet, ClientViewDetail, MailingViewDetail


router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'mailings', MailingViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('clients/detail/<int:pk>/', ClientViewDetail.as_view()),
    path('mailing/detail/<int:pk>/', MailingViewDetail.as_view()),
]
