from unittest.mock import MagicMock
from types import ModuleType
from clearskies import Model
from ...actions.sms import SMS as BaseSMS
class SMS(BaseSMS):
    calls = None

    def __init__(self, twilio, di) -> None:
        # we don't need this, but let's keep it just in case
        self._twilio = twilio

        self.twilio = MagicMock()
        self.twilio.messages = MagicMock()
        self.twilio.messages.create = self.twilio_call
        self.di = di

    @classmethod
    def mock(cls, di):
        cls.calls = []
        di.mock_class(BaseSMS, SMS)

    @classmethod
    def twilio_call(cls, **kwargs):
        cls.calls.append({**kwargs})
