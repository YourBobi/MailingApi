from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics
import datetime
import pytz

from .models import Mailing, Client, Message
from .serializers import MailingSerializer, ClientSerializer, MessageSerializer
from .send_message import send_message

URL = "https://probe.fbrq.cloud/v1/send/"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTIzNjc3MDksImlzcyI6ImZhYnJpcXVlIiwib" \
                "mFtZSI6InN0aWxsX2RvZyJ9.pmVA7XAuDjqECNdK-Xia3IvtMS8MKI1BDkjcaGWFhOU"


class ClientViewSet(viewsets.ModelViewSet):
    """
    Set new client
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ClientViewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Updates and delete to client attribute data
    """
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    """
    Set new message
    """
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    @action(detail=False, methods=['get'])
    def send_messages(self, request):
        """
        Send messages to some api
        """
        messages = Message.objects.filter(sending_status=False).all()
        number_of_sending_msg = 0

        for message in messages:
            timezone = pytz.timezone(message.client.timezone)
            now = datetime.datetime.now(timezone)
            if message.mailing.date_start <= now <= message.mailing.date_end \
                    and message.mailing.time_start <= now.time() <= message.mailing.time_end:
                data = {
                    'id': message.id,
                    "phone": message.client.phone_number,
                    "text": message.mailing.text_for_client
                }
                send_message(data=data, url=URL, token=TOKEN)
                number_of_sending_msg += 1

        content = {'The number of messages sent': number_of_sending_msg}
        return Response(content)


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    @action(detail=True, methods=['get'])
    def info(self, request, pk=None):
        """
        Summary data for a specific mailing list
        """
        queryset_mailing = Mailing.objects.all()
        get_object_or_404(queryset_mailing, pk=pk)
        queryset = Message.objects.filter(mailing_id=pk).all()
        serializer = MessageSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def full_info(self, request):
        """
        Summary data for all mailings
        """
        total_count = Mailing.objects.count()
        mailing = Mailing.objects.values('id')
        content = {'Total number of mailings': total_count,
                   'The number of messages sent': ''}
        result = {}

        for row in mailing:
            res = {'Total messages': 0, 'Sent': 0, 'No sent': 0}
            mail = Message.objects.filter(mailing_id=row['id']).all()
            group_sent = mail.filter(sending_status=True).count()
            group_no_sent = mail.filter(sending_status=False).count()
            res['Total messages'] = len(mail)
            res['Sent'] = group_sent
            res['No sent'] = group_no_sent
            result[row['id']] = res

        content['The number of messages sent'] = result
        return Response(content)


class MailingViewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
        Updates and delete to mailing attribute data
    """
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()
