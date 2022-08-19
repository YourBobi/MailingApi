from django.db import models
import pytz
from django.utils import timezone


class Mailing(models.Model):
    date_start = models.DateTimeField(verbose_name='Date of the newsletter launch')
    date_end = models.DateTimeField(verbose_name='Date of the end of the mailing list')
    time_start = models.TimeField(verbose_name='Time of the newsletter launch')
    time_end = models.TimeField(verbose_name='Time of the end of the mailing list')
    text_for_client = models.CharField(verbose_name='Text for client', max_length=255)
    tag = models.CharField(max_length=100, verbose_name='Search by tags', blank=True)
    mobile_operator_code = models.CharField(verbose_name='Search by mobile operator',
                                            max_length=3, blank=True)

    @property
    def to_send(self):
        now = timezone.now()
        if self.date_start <= now <= self.date_end:
            return True
        else:
            return False

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'


class Client(models.Model):
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    phone_number = models.CharField(verbose_name='Phone number', unique=True, max_length=11)
    mobile_operator_code = models.CharField(verbose_name='Mobile operator', max_length=3, editable=False)
    tag = models.CharField(verbose_name='Search tags', max_length=100, blank=True)
    timezone = models.CharField(verbose_name='Time zone', max_length=32, choices=TIMEZONES, default='UTC')

    def save(self, *args, **kwargs):
        self.mobile_operator_code = str(self.phone_number)[1:4]
        return super(Client, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Message(models.Model):
    time_create = models.DateTimeField(verbose_name='Time create', auto_now_add=True)
    sending_status = models.BooleanField(verbose_name='Sending status')
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='messages')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='messages')

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
