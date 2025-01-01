from uuid import uuid3, NAMESPACE_URL, NAMESPACE_DNS
from base64 import b64encode, urlsafe_b64encode

def shorten(url: str, namespace=NAMESPACE_DNS) -> str:
    return urlsafe_b64encode(uuid3(namespace, url).bytes).decode()

if __name__ == "__main__":
    url = "preet"
    print(urlsafe_b64encode(shorten("Preet", NAMESPACE_DNS)))