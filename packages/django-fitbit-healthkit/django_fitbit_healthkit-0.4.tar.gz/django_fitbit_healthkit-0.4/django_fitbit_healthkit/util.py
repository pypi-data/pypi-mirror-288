import base64
import hashlib
import hmac

from django.conf import settings


def verify_fitbit_signature(sig: str, data: str) -> bool:
    return sig == make_digest(settings.FITBIT_CLIENT_SECRET + "&", data)


# https://gist.github.com/heskyji/5167567b64cb92a910a3
def make_digest(key: str, message: str) -> str:
    key = bytes(key, "UTF-8")
    message = bytes(message, "UTF-8")

    digester = hmac.new(key, message, hashlib.sha1)
    signature1 = digester.digest()

    signature2 = base64.urlsafe_b64encode(signature1)

    return str(signature2, "UTF-8")


def encoded_secret(client_id: str, client_secret: str) -> str:
    return base64.b64encode(f"{client_id}:{client_secret}".encode("latin1")).decode(
        "latin1"
    )


def extract_active_from_total(total: float, METs_sum: int, minutes: int) -> float:
    """
    fitbit returns the calories burned in the interval, so we need to subtract the basal calories
    the METs returned by fitbit has a bug where it SUMS the value
    AND their METs are multiplied by 10 so they can store ints for precision level of 1
    so we take minutes * 10 to get the baseline METs for fitbit
    for a 15 minute interval, the baseline METs is 150
    we then take the relative percentage of the METs for the interval / 150, subtracting out 1
    (100%, the baseline)
    so METs of 150 for a 15 minute interval should be value * 0
    so METs of 300 for a 15 minute interval should be value * 1
    so METs of 450 for a 15 minute interval should be value * 2
    """
    # don't divide by 0
    if METs_sum == 0:
        return 0.0
    minutes_10 = minutes * 10
    # don't return negative
    if minutes_10 > METs_sum:
        return 0.0
    return total * ((METs_sum - minutes_10) / METs_sum)
