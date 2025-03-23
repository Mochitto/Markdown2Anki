from typing import Any, Callable
from unittest.mock import call, patch

import pytest
import requests

from markdown2anki.ankiconnect import AnkiConnect


@pytest.fixture
def ac(mocker):
    """Setup fixture for initializing AnkiConnect and mocking the initial connection."""

    class Response:
        def __init__(self, status_code, text):
            """A simple class to mock the response object."""
            self.status_code = status_code
            self.text = text

    mocker.patch(
        "requests.get",
        return_value=Response(status_code=200, text="AnkiConnect v.6"),
    )
    return AnkiConnect()


def mock_send_cmd(callback: Callable, args_and_rets: list[tuple[Any, Any]]) -> Any:
    """Call the callback and mock the ._send_cmd method with given args and return vals.

    Use this function whenever you want to test a function that calls the ._send_cmd
    method of the AnkiConnect class. With args_and_rets you can specify the arguments
    that are passed to the mocked ._send_cmd method and the return values that are
    returned by it.

    Args:
        callback:       The function that should be called. This function should
                        contain the code that you want to test.
        args_and_rets:  List of tuples. First element in tuple are the function
                        arguments that we expect that the mocked function will be
                        called with. If several function arguments are needed pack them
                        into a tuple or dict. Second element is what the mocked
                        function will return.


    Returns: The returned value from the callback


    """
    with patch("markdown2anki.AnkiConnect._send_cmd") as send_cmd:
        send_cmd.side_effect = [ret for _, ret in args_and_rets]

        ret = callback()

        def convert_args(arg_and_ret):
            arg, _ = arg_and_ret
            if isinstance(arg, tuple):
                return call(*arg)
            elif isinstance(arg, dict):
                return call(**arg)
            else:
                return call(arg)

        send_cmd.assert_has_calls(list(map(convert_args, args_and_rets)))

    return ret


def test_mocking_first_connection_test(ac):
    """Test the first connection to AnkiConnect."""
    requests.get.assert_called_once_with(ac.url)


def test_checking_for_existing_deck(ac):
    """Test checking for an existing deck."""

    def cb():
        ac._check_for_deck("existing_deck")

    mock_send_cmd(cb, [("deckNames", ["existing_deck", "some_other_deck"])])


def test_checking_for_non_existing_deck(ac):
    """Test checking for a non-existing deck and creating it."""
    args_and_rets = [
        ("deckNames", ["existing_deck", "some_other_deck"]),
        (("createDeck", {"deck": "non_existing_deck"}), 1519323742721),
    ]

    def cb():
        ac._check_for_deck("non_existing_deck")

    mock_send_cmd(cb, args_and_rets)


def test_checking_for_existing_note_type(ac):
    """Test checking for an existing note type."""

    def cb():
        return ac._does_note_type_exist("existing_note_type")

    ret = mock_send_cmd(
        cb, [("modelNames", ["existing_note_type", "some_other_note_type"])]
    )

    assert ret is True


def test_checking_for_non_existing_note_type(ac):
    """Test checking for an non-existing note type."""

    def cb():
        return ac._does_note_type_exist("non_existing_note_type")

    ret = mock_send_cmd(
        cb, [("modelNames", ["existing_note_type", "some_other_note_type"])]
    )

    assert ret is False
