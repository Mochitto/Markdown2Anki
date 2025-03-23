import logging
import sys
import json

import requests

logger = logging.getLogger(__name__)


class AnkiCard:
    """Class representing a card that can be uploaded to Anki."""

    def __init__(
        self,
        deck_name: str,
        note_type: str,
        fields: dict,
        tags: list[str] | None = None,
    ) -> None:
        self.deck_name = deck_name
        self.note_type = note_type
        self.fields = fields
        self.tags = tags

    def to_api(self) -> dict:
        """Return dict required by the addNote API call."""
        d = {
            "note": {
                "deckName": self.deck_name,
                "modelName": self.note_type,
                "fields": self.fields,
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "all",
                    "duplicateScopeOptions": {
                        "deckName": self.deck_name,
                        "checkChildren": True,
                        "checkAllModels": True,
                    },
                },
            },
        }

        if self.tags:
            d["note"]["tags"] = self.tags

        return d


class AnkiMediaFile:
    """Class representing a media file that can be uploaded to Anki."""

    def __init__(self, filename, path) -> None:
        # Name of the file.
        self.filename = filename
        # File location, can be absolute or relative.
        self.path = path

    def to_api(self) -> dict:
        """Return dict required by the storeMediaFile API call."""
        return {"filename": self.filename, "path": self.path}


class AnkiConnect:
    """Class containing all methods for interracting with the AnkiConnect plugin."""

    def __init__(
        self,
        url: str = "http://127.0.0.1:8765",
    ):
        self.url = url
        # We want to use the latest AnkiConnect API version.
        self.api_ver = 6

        ok, msg = self._is_running()
        if not ok:
            raise Exception(msg)

    def _is_running(self):
        """
        Check if AnkiConnect is running.

        Return True if AnkiConnect is running and the API version is correct.
        """
        msg = ""
        try:
            rsp = requests.get(self.url)
        except requests.exceptions.ConnectionError:
            msg = (
                f"🚨 AnkiConnect plugin was not detected on {self.url}.\n"
                "Make sure that Anki is running in the background and that AnkiConnect "
                "plugin is installed.\n"
                "For additional information, please refer to the AnkiConnect "
                "documentation: \n\n\thttps://foosoft.net/projects/anki-connect\n\n"
                "Exiting..."
            )
            return False, msg
        except (requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
            msg = (
                f"🚨 Given AnkiConnect URL ({self.url}) is not in correct format.\n"
                "Make sure that the URL is in the following format: "
                "http://IP_ADDRESS:PORT\n"
                "Exiting..."
            )
            return False, msg

        if rsp.status_code != 200:
            msg = (
                f"🚨 AnkiConnect plugin was detected on {self.url}, but failed to get "
                "correct response.\n"
                "Make sure that Anki is running in the background and that AnkiConnect "
                "plugin is installed.\n"
                "Exiting..."
            )
            return False, msg

        if (
            json.loads(rsp.text).get("apiVersion", "")
            != f"AnkiConnect v.{self.api_ver}"
        ):
            msg = (
                f"🚨 AnkiConnect plugin was detected on {self.url}, but the API version "
                f"is not correct. Expected version: v.{self.api_ver}.\n"
                f"This shouldn't happen, please report this issue to Markdown2Anki's "
                "GitHub\n"
                "Exiting..."
            )

            return False, msg

        return True, msg

    def upload_cards(
        self,
        cards: dict,
        deck_name: str,
        note_type_basic: str,
        note_type_cloze: str,
        tags: list[str] = [],
    ):
        """Upload cards to Anki."""
        self._check_for_deck(deck_name)

        for note_type in [note_type_basic, note_type_cloze]:
            if not self._does_note_type_exist(note_type):
                msg = (
                    f"🚨 Note type {note_type} doesn't exist in Anki.\n"
                    "Correct it in the input markdown file.\n"
                    "Exiting..."
                )
                logger.error(msg)
                sys.exit(1)

        def basic_card(fields) -> AnkiCard:
            return AnkiCard(
                deck_name,
                note_type_basic,
                fields,
                tags,
            )

        def cloze_card(fields) -> AnkiCard:
            return AnkiCard(
                deck_name,
                note_type_cloze,
                fields,
                tags,
            )

        def convert_image(image: tuple[str, str]) -> AnkiMediaFile:
            return AnkiMediaFile(image[0], image[1])

        anki_cards = []
        anki_cards += list(map(basic_card, cards["cards"]))
        anki_cards += list(map(cloze_card, cards["cards_with_clozes"]))

        media_files = list(map(convert_image, cards["images_to_copy"].items()))

        if anki_cards:
            logger.info("📡 Sending cards to Anki...")
            for idx, card in enumerate(anki_cards):
                self._upload_card(card, idx + 1)

        if media_files:
            logger.info("📺 Sending images to Anki...")
            for idx, media_file in enumerate(media_files):
                self._upload_media_file(media_file, idx + 1)

    def _check_for_deck(self, deck_name: str):
        """Check if deck exists in Anki. If it doesn't it creates it."""
        rsp = self._send_cmd("deckNames")

        if deck_name not in rsp:
            self._send_cmd("createDeck", {"deck": deck_name})
            logger.info(f"🔨 Created deck '{deck_name}' in Anki")

    def _does_note_type_exist(self, note_type: str) -> bool:
        """Check if note type exists. Return True if it does, False otherwise.

        modelNames action actually checks for the Note type in AnkiConnect. It looks
        wrong but it is correct.
        """
        return note_type in self._send_cmd("modelNames")

    def _upload_card(self, card: AnkiCard, idx: int):
        res, msg = self._send_req("addNote", card.to_api())

        if res:
            logger.info(f"|--- ✅ Sent card number {idx}")
            return

        if msg == "cannot create note because it is a duplicate":
            logger.info(f"|--- 🔁 Card number {idx} already exists in Anki.")
            return

        logger.error(f"Failed to upload card {idx} to Anki: {msg}")
        sys.exit(1)

    def _upload_media_file(self, media_file: AnkiMediaFile, idx: int):
        res, msg = self._send_req("storeMediaFile", media_file.to_api())

        if res:
            logger.info(f"|--- ✅ Sent image number {idx}")
            return

        logger.error(f"Failed to upload image number {idx} to Anki: {msg}")
        sys.exit(1)

    def _send_cmd(self, action: str, params: dict | None = None) -> dict:
        """Wrapper around _send_req that only returns response.

        It will assert that the result was successful and return just the response.
        In the case that the result was not successful it will log the error and exit.

        Use this method when you expect the command to always succeed, any error is
        considered as a mistake in the code.

        If it is possible that the command can fail use _send_req instead.
        """
        res, rsp = self._send_req(action, params)

        if res:
            return rsp

        error = (
            f"Sent command '{action}' to AnkiConnect plugin, but failed to get "
            "successful response.\n"
            "Sent parameters:\n"
            f"{params}\n\n"
            "Received error:\n"
            f"{rsp}\n\n"
            "Exiting..."
        )
        logger.error(error)
        sys.exit(1)

    def _send_req(self, action: str, params: dict | None = None) -> tuple[bool, dict]:
        """
        Send HTTP request to the AnkiConnect plugin.

        Return tuple, where:

            First element is result:
                If True, the request was successfully processed by the AnkiConnect
                plugin.
                Otherwise, the request failed.

            Second element is response:
                If result was True it contains response data returned by the
                AnkiConnect plugin.
                Otherwise it contains error message.

        For AnkiConnect API refer to the:
            https://foosoft.net/projects/anki-connect/
        """
        req = {
            "action": action,
            "version": self.api_ver,
        }

        if params:
            req["params"] = params

        try:
            rsp = requests.post(self.url, json=req).json()
            if rsp["error"]:
                return (False, rsp["error"])
            return (True, rsp["result"])

        except requests.exceptions.ConnectionError:
            error = (
                "🚨 Failed to get response from AnkiConnect plugin.\n"
                "Make sure that Anki is running in the background and that AnkiConnect "
                "plugin is installed.\n"
                "For additional information, please refer to the AnkiConnect "
                "documentation: \n\n\thttps://foosoft.net/projects/anki-connect\n\n"
                "Exiting..."
            )
            logger.error(error)
            sys.exit(1)
