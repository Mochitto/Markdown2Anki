import logging

import requests

logger = logging.getLogger(__name__)


def ankiconnect_send_request(action: str, params: dict) -> (bool, str):
    """
    Send HTTP request to the AnkiConnect plugin.

    Return tuple, where:
        success: If True, the request was successfully processed by the AnkiConnect
        plugin.
        error: Contains error message returned by the AnkiConnect plugin. Valid only if
        success is False.

    For AnkiConnect API refer to the:
    https://github.com/FooSoft/anki-connect#supported-actions
    """
    request = {
        "action": action,
        "params": params,
        # We want to use the latest AnkiConnect API version.
        "version": 6,
    }
    response = requests.post("http://localhost:8765", json=request).json()

    return (False if response["result"] is None else True, response["error"])


def create_note(deck_name: str, model_name: str, fields: str) -> dict:
    """
    Create note field, required by the addNote API call.
    """
    return {
        "note": {
            "deckName": deck_name,
            "modelName": model_name,
            "fields": fields,
            "options": {
                "allowDuplicate": False,
                "duplicateScope": "all",
                "duplicateScopeOptions": {
                    "deckName": deck_name,
                    "checkChildren": True,
                    "checkAllModels": True,
                },
            },
        },
    }


def send_to_anki(cards: dict):
    """ """
    logger.info("📡 Sending cards to Anki...")

    # TODO: Creation of notes below is quite ugly for now but it works.
    # We need a way to get deck_name and notetype, they should be provided by the caller.
    # When that is done, the hardcoded values can be removed
    def basic_note(note_fields):
        return create_note("Work notes", "Markdown2Anki - Basic", note_fields)

    def cloze_note(note_fields):
        return create_note("Work notes", "Markdown2Anki - Cloze", note_fields)

    notes = []
    notes += list(map(basic_note, cards["cards"]))
    notes += list(map(cloze_note, cards["cards_with_clozes"]))

    # TODO: There are many reasons why the ankiconnect_send_request would fail.
    # We need some general direction on:
    # - Are there some validation steps that should be done before starting to send
    # things? (like to check if the deck and note type even exist?)
    # - How should errors be handled? Should be we abort on an error, or keep going?

    for index, note in enumerate(notes):
        sent, error = ankiconnect_send_request("addNote", note)
        if sent:
            logger.info(f"|--- ✅ Sent card number {index + 1}")
        else:
            logger.info(f"|--- ❌ Failed to send the card number {index + 1}...")
            logger.error(f"|------- ERROR: {error}")

    logger.info("📺 Sending images to Anki...")
    for index, image in enumerate(cards["images_to_copy"].items()):
        sent, error = ankiconnect_send_request(
            "storeMediaFile", {"filename": image[0], "path": image[1]}
        )
        if sent:
            logger.info(f"|--- ✅ Sent image item number {index + 1}")
        else:
            logger.info(f"|--- ❌ Failed to send the media number {index + 1}...")
            logger.error(f"|------- ERROR: {error}")
