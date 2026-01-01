import requests

def send_push(token, title, body):
    requests.post(
        "https://exp.host/--/api/v2/push/send",
        json={"to": token, "title": title, "body": body}
    )
