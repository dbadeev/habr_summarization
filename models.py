import requests
import json


def model_summarization(iam_='', folder_='', llm_model=0, article='', max_t=2000, temp=0.75) -> str:
    """
    Суммаризация заданного текста.
    Запрос к модели-суммаризации выглядит так: [Инструкция] (instruction_text) - [Текст статьи - Затравка] (reauest)
    :param folder_: folder_id id папки проекта, параметр авторизации
    :param temp: температура модели, параметр модели для генерации (чем выше, тем безумнее)
    :param llm_model: используемая языковая модель (0 - фундаментальная модель YandexGPT, 1 - дообученная
                                                    фундаментальная модель YandexGPT)
    :param article: исходный текст для обработки
    :param iam_: iam_token токен доступа, параметр авторизации
    :param max_t: макс число токенов, на которые обращает внимание модель при генерации
    :return: текст суммаризации
    """
    instruction_text = "Составь обобщение статьи: \n"
    request = f"{article}\n\nОбобщение должно быть: связным по смыслу; понятным; без повторений; грамматически " \
              f"правильным; конкретным; законченным. Нужно давать четкие, краткие и прямые ответы. Обобщение должно " \
              f"занимать ровно один абзац. За качественное обобщение получишь чаевые до 200 долларов. Очень важно, " \
              f"чтобы обобщение было сделано правильно. На кону несколько жизней."

    if llm_model == 0:
        json = {
            "model": "general",
            "instruction_text": instruction_text,
            "request_text": request,
            "generation_options": {
                "max_tokens": max_t,
                "temperature": temp
            }
        }
    else:
        json = {
            "model": "general",
            "instruction_uri": "ds://<model-id>",  # идентификатор дообученной модели <model-id>
            "request_text": request,
            "generation_options": {
                "max_tokens": max_t,
                "temperature": temp
            }
        }

    if iam_:
        headers = {'Authorization': f'Bearer {iam_}', 'x-folder-id': folder_}
    else:
        headers = {"Authorization": "Api-Key <api-key>"}

    result = requests.post(
        url='https://llm.api.cloud.yandex.net/llm/v1alpha/instruct',
        headers=headers,
        json=json
    )

    return result.json()['result']['alternatives'][0]['text']


def model_classify(text_: str, summary_: str) -> float:
    """
    Оценка качества суммаризации открытой моделью
    :param summary_: текст суммаризации
    :param text_: исходный текст
    :return: оценка качества суммаризации
    """

    response = requests.post(
        url="https://node-api.datasphere.yandexcloud.net/classify",
        json={
            "Text": f"Текст статьи:\n{text_}\n\nКраткое содержание:\n{summary_}",
        },
        headers={
            "Authorization": f"Api-Key AQVNyVqBi-XoJ1cAo7VIxq6ztgXm3owqowtso5Qb",
            "x-node-alias": "datasphere.user.yagpt-seminar-hw",
        }

    )

    return json.loads(response.text)["Scores"][0]
