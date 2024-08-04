import request


class TelegramBot:
    def __init__(self, token: str, auto_offset: bool = True):
        self.__base_url = f"https://api.telegram.org/bot{token}/"
        self.auto_offset = auto_offset
        self.last_update_id = -1

    def get_updates(self,
                    offset: int | None = None,
                    limit: int | None = None,
                    timeout: int | None = 30) -> dict:

        url = self.__base_url + "getUpdates"
        data = {}

        if offset:
            data["offset"] = offset
        elif self.auto_offset:
            data["offset"] = self.last_update_id + 1

        if limit:
            data["limit"] = limit

        if timeout:
            data["timeout"] = timeout

        response = request.get(url, data or None)
        updates = response.get("result", []) if response.get("ok") else None
        update_ids = map(lambda upd: upd.get("update_id"), updates)
        self.last_update_id = max((self.last_update_id, *update_ids))

        return updates

    def send_message(self, chat_id: str, text: str) -> dict | None:
        url = self.__base_url + "sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
        }
        return request.post(url, data)

    # def send_animation(self):
    #     url = self.__base_url + "sendAnimation"


if __name__ == "__main__":
    import os
    bot = TelegramBot(os.environ["TOKEN"], auto_offset=True)
    chat_id_ = os.environ["CHAT_ID"]

    bot.send_message(chat_id_, "test")
    ups = bot.get_updates(timeout=None)

