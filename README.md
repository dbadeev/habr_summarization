# Суммаризация статей Habr

Мы собрали несколько тысяч статей с Habr, для 100 из них предстоит построить автоматическую абстрактивную суммаризацию. 
### Что нужно сделать
 - Построить суммаризации для 100 статей из файла `test_articles_clear_100.json`
 - Суммаризации оформить в нужном формате и отправить на проверку
 

### Как оценивается качество
- Качество будет оцениваться моделью, обученной на метрику **SEAHORSE Q6 Concise** 
    - Статья https://arxiv.org/abs/2305.13194
    - Данные и метрики от авторов https://github.com/google-research-datasets/seahorse
- Про обучение модели качества:
        - Мы взяли RU и EN данные из статьи SEAHORSE: A Multilingual, Multifaceted Dataset for Summarization Evaluation https://arxiv.org/abs/2305.13194
        - Обучили модель-метрику предсказывать Q6 Concise из датасета статьи (как самую высокоуровневую метрику из предложенных)
        - 10% данных ушло на dev/test
        - 90% данных ушло на обучение модели (мы обучили 2 модели, открытую и закрытую, каждая из моделей обучена на 60% данных от полного датасета)

- На вход метрике-модели текст подается в следующем формате: `"Текст статьи:\n" + Text + "\n\n" + "Краткое содержание:\n" + Summary as metric_input`

### Критерий успешного прохождения
 - Получить качество суммаризаций не хуже (с учетом статзначимости), чем у выбранного нами бейзлайна по оценке **закрытой** моделью. 
 - Качество бейзлайна по оценке открытой моделью `=0.557`
 - <i>Примечание.</i> Почему используется закрытая модель? Так как тестовые данные и модель для оценки качества открыты, то можно переобучиться и обмануть открытую модель оценки качества методом перебора.

### Что в архиве
- `test_articles_clear_100.json` - статьи, которые нужно суммаризовать.
- `train_data.json` - примеры различных суммаризаций с оценкой открытой моделью, которые можно использовать для дообучения при необхдимости.
- `example.ipynb` - jupyter ноутбук с примерами чтения данных и того, как записывать решение, то есть выходного формата. Также приведен пример запроса в API для замера качества суммаризаций во время разработки решения. 

### Формат отправки выполненного задания
- `json lines` - в каждой строке json вида `{'id': AAA, 'summary': "BBB"}` (есть в примере)
