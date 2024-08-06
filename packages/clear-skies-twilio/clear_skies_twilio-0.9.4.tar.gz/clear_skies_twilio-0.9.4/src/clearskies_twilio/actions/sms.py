import re
from typing import Callable, List, Optional, Union

import clearskies

class SMS:
    def __init__(self, twilio, di) -> None:
        self.twilio = twilio
        self.di = di

    def configure(
        self,
        from_number: Optional[Union[str, Callable]] = None,
        to_number: Optional[Union[str, Callable, List[Union[str, Callable]]]] = None,
        message: Optional[Union[str, Callable]] = None,
        when: Optional[Callable] = None,
    ) -> None:
        """Configure the rules for this SMS notification."""
        self._required_str_or_callable_check(message, "message")
        self._required_str_or_callable_check(from_number, "from_number")
        if isinstance(to_number, list):
            for (index, to_number_value) in enumerate(to_number):
                self._required_str_or_callable_check(to_number_value, "to_number")
        else:
            self._required_str_or_callable_check(to_number, "to_number")

        if when and not callable(when):
            raise ValueError("Config 'when' for twilio.actions.sms should be a callable, but isn't.")

        self.when = when
        self.message = message
        self.from_number = from_number
        self.to_number = to_number

    def _required_str_or_callable_check(self, item: Union[str, Callable], label: str) -> None:
        if not item:
            raise ValueError(f"Config '{label}' for twilio.actions.sms is required, but was not provided.")

        if not isinstance(item, str) and not callable(item):
            bad_type = item.__class__.__name__
            raise ValueError(
                f"Config '{label}' for twilio.actions.sms should be a string or a callable, but instead is a '{bad_type}'"
            )
        return

    def __call__(self, model: clearskies.Model) -> None:
        """Send a notification as configured."""
        if self.when and not self.di.call_function(self.when, model=model):
            return

        from_number = self._resolve_number(self.from_number, "from_number", model)
        if not from_number:
            raise ValueError("I did not receive a from number")
        from_number = from_number[0]
        to_numbers = self._resolve_numbers(self.to_number, "to_number", model)
        if not from_number or not to_numbers:
            return
        message = self._resolve_message(self.message, model)

        for to_number in to_numbers:
            self.twilio.messages.create(**{
                "to":to_number,
                "from_":from_number,
                "body":message,
            })

    def _resolve_numbers(self, numbers: Union[str, Callable, List[Union[str, Callable]]], label: str, model: clearskies.Model) -> str:
        if not isinstance(numbers, list):
            numbers = [numbers]
        resolved_numbers = []
        for number in numbers:
            resolved = self._resolve_number(number, label, model)
            resolved_numbers.extend(resolved)
        return resolved_numbers

    def _resolve_number(self, number: Union[str, Callable], label: str, model: clearskies.Model) -> List[str]:
        """
        Convert self.from_number or self.to_number to a list of actual phone numbers.

        We can receive a few things:

         1. A phone number
         2. The name of a column from the model
         3. A callable that returns a phone number(s)

        Note that the actual phone numbers may not be in the correct format expected by twilio.
        """
        model_label = model.id_column_name + ": " + model.get(model.id_column_name)
        if callable(number):
            numbers = self.di.call_function(number, model=model)
            if not numbers:
                return []
            if isinstance(numbers, str):
                numbers = [numbers]
            elif isinstance(numbers, list):
                if not all(isinstance(item, str) for item in numbers):
                    raise ValueError(f"Error with clearskies_twilio.actions.sms: I executed the callable attached to '{label}' but the list it returned contained non-strings.  The callable must return a phone number as a string, or a list of phone numbers as strings.")
            else:
                raise ValueError(f"Error with clearskies_twilio.actions.sms: I executed the callable attached to '{label}' but it did not return a valid value.  The callable must return a phone number as a string, or a list of phone numbers as strings.")
        else:
            if not number:
                return []
            # do we have a column name?
            if number in model.columns():
                numbers = model.get(number)
                if not isinstance(numbers, str):
                    raise ValueError(f"Error with clearskies_twilio.actions.sms: I fetched a column called '{label}' for model {model_label}, hoping for a phone number, but it returned a non-string.  The column must return a phone number as a string.")
                numbers = [numbers]
            else:
                numbers = [number]

        # now make sure we have a twilio friendly number
        final_numbers = []
        for number in numbers:
            number = re.sub(r"\D", "", number)
            if not number:
                raise ValueError(f"Error with clearskies.twilio.actions.sms: while fetching the '{label}' for model {model_label} I ended up with something that just doesn't look like a phone number.")
            if len(number) == 10:
                number = f"1{number}"
            final_numbers.append(f"+{number}")
        return final_numbers

    def _resolve_message(self, message: Union[Callable, str], model: clearskies.Model) -> str:
        """Build the string for the message given the model."""
        if callable(message):
            message = self.di.call_function(message, model=model)
            if not message:
                raise ValueError(f"Error with clearskies.twilio.actions.sms: I executed the callable attached to 'message' but it returned a non-value.  The callable must return a message as a string.  In case this helps, you can provide a callable to 'when' and have it return false in csaes where you don't want a message sent.")
            if not isinstance(message, str):
                raise ValueError(f"Error with clearskies_twilio.actions.sms: I executed the callable attached to 'message' but it did not return a string.  The callable must return a message as a string.")

        return message
