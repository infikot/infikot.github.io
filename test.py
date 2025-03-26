import asyncio
import aiohttp
import uuid

async def generate_qudata(text: str, trying: int or None = 0) -> str | None:
    """
    https://qudata.com/ru/chat-gpt/
    Лимит: 100 символов
    Страна: Украина
    Нейросеть: ?
    """

    url = "https://qudata.com/ru/includes/sendmail/chat.php"

    headers = {
        'accept': '*/*',
        'accept-language': 'ru',
        'dnt': '1',
        'origin': 'https://qudata.com',
        'priority': 'u=1, i',
        'referer': 'https://qudata.com/ru/chat-gpt/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
        'x-requested-with': 'XMLHttpRequest'
    }

    random_dialog_id = str(uuid.uuid4())
    random_user_id = str(uuid.uuid4())

    payload = {
        'message': text,
        'dialogs[0][role]': 'user',
        'dialogs[0][content]': text,
        'dialogid': random_dialog_id,
        'userid': random_user_id
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.post(url, data=payload) as response:
                if response.status == 200:
                    ai_resp = await response.text()
                    if ai_resp == "limit25000" or trying >= 5:
                        ai_resp = await generate_qudata(text, trying+1)
                        return ai_resp
                    elif ai_resp != "limit25000":
                        return ai_resp
                    else:
                        return None

                else:
                    print(f"Ошибка: Сервер ответил со статусом {response.status}")
                    return None

        except aiohttp.ClientError as e:
            print(f"Ошибка во время http запроса: {e}")
            return None

async def generate_mitup(text: str) -> str | None:
    """
    https://ai.mitup.ru/chatgpt-free
    Лимит: 1-3 запрос(а)/сутки
    Страна: Россия
    Нейросеть: gemini-1.5-flash-8b
    """

    url = "https://ai.mitup.ru/ask"

    headers = {
        'accept': '*/*',
        'accept-language': 'ru',
        'dnt': '1',
        'origin': 'https://ai.mitup.ru',
        'priority': 'u=1, i',
        'referer': 'https://ai.mitup.ru/chatgpt-free',  # Важный реферер из примера
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
        'x-requested-with': 'XMLHttpRequest'
    }

    form_data = aiohttp.FormData()
    form_data.add_field('user_id', 'null')
    form_data.add_field('input_text', text)
    form_data.add_field('url', '/chatgpt-free')
    form_data.add_field('chats_id', '0')
    form_data.add_field('model', 'gemini-1.5-flash-8b')
    form_data.add_field('context', 'false')
    form_data.add_field('sessid', 'null')

    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            async with session.post(url, data=form_data) as response:
                if response.status == 200:
                    try:
                        json_response = await response.json()
                        bot_message = json_response.get('bot_message')

                        if bot_message and isinstance(bot_message, dict):
                            ai_resp = bot_message.get('text')

                            # --- Улучшенная проверка ---
                            if isinstance(ai_resp, str) and ai_resp: # Убедимся, что строка не пустая
                                return ai_resp
                            elif ai_resp is None:
                                return None
                            else:
                                return None

                        else:
                            return None

                    except aiohttp.ContentTypeError:
                        return None
                    except Exception as e_json:
                        print(f"Ошибка парсинга JSON: {e_json}")
                        return None
                else:
                    print(f"Ошибка: Сервер ответил со статусом {response.status}")
                    print("Не удалось прочитать тело ответа.")
                    return None

        except aiohttp.ClientError as e_http:
            print(f"Ошибка во время http запроса к ai.mitup.ru: {e_http}")
            return None
        except Exception as e_general:
             print(f"Произошла непредвиденная ошибка: {e_general}")
             return None

async def main():

    try_to = "Who are u?"
    print(f"\n\nUser: {try_to}\nAll AI's:\n\n")

    # await generate_qudata(text: str)
    qudata = await generate_qudata(try_to)
    print(f"QuData: {qudata}")

    # await generate_mitup(text: str)
    mitup = await generate_mitup(try_to)
    print(f"mitup: {mitup}")




if __name__ == "__main__":
    asyncio.run(main())