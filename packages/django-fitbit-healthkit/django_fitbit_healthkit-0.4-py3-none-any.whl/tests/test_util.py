import os

import django
from django.test import TestCase, override_settings

from django_fitbit_healthkit.util import (encoded_secret,
                                          extract_active_from_total,
                                          make_digest, verify_fitbit_signature)

# use the same app's settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sample.settings")
django.setup()


class SignatureTestCase(TestCase):
    @override_settings(
        FITBIT_CLIENT_SECRET="key",
    )
    def test_verify_fitbit_signature(self):
        assert verify_fitbit_signature("6a6Jz8J2Z6vq1n4Gv5JyCQ==", "data") is False
        assert verify_fitbit_signature('Hc74fuYQh-M5l3zdafPZ-Sdi-pY=', "data") is True


def test_make_digest():
    assert make_digest("key&", "data") == 'Hc74fuYQh-M5l3zdafPZ-Sdi-pY='


def test_encoded_secret():
    assert (
        encoded_secret("client_id", "client_secret")
        == "Y2xpZW50X2lkOmNsaWVudF9zZWNyZXQ="
    )


def test_extract_active_from_total():
    assert extract_active_from_total(1, 0, 1) == 0
