import requests
from .models import Message


def send_message(data: dict, url: str, token: str):
    print(url)
    header = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'}
    try:
        requests.post(url=url + str(data['id']), headers=header, json=data)
    except requests.exceptions.RequestException as exc:
        raise exc
    else:
        Message.objects.filter(pk=data['id']).update(sending_status=True)
