# Скачивание изображений с сайтов NASA, SpaceX и публикация их в телеграм канале.

Программа позволяет скачивать изображения с сайтов NASA и SpaceX и публиковать их в телеграм канал.

### Как установить

Для указания папки, куда необходимо сохранять скаченные изображения, используйте переменную окружения `PATH_TO_IMAGES`, если не указана, используется путь по умолчанию `./images/`.  
Для получения изображений с сайта NASA, необходимо получить TOKEN на сайте https://api.nasa.gov и сохранить его в переменную окружения `NASA_TOKEN`.  
Для отправки изображений в канал, необходимо создать бота телеграм и полученный TOKEN сохранить в переменную окружения `TELEGRAM_TOKEN`.  
Для определения канала, куда необходимо отправлять изображения, нужно заполнить переменную `ID_TELEGRAM_CHANNEL`.  

Python3 должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запускать
```
python3 main.py
```

### Настройка времени срабатывания
Для указания времени когда программа сработает, необходимо указать количество секунд в переменную окружения
TIMEOUT, если переменная окружения не указана, то время срабатывания по умолчанию становится равным одним суткам.

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).