# Автоконтент

**Настраиваем окружение**
 1. Создаём учётки на [Google Console](https://console.cloud.google.com/project?pli=1), [Yandex Speechkit](https://cloud.yandex.ru/services/speechkit), [OpenAI](https://chat.openai.com/)
 2. На гугле подключаем сервис google-drive, на яндексе - Yandex SpeechKit
 3. Заполняем .env-файлы переменными для Google, Yandex и ChatGPT 
 4. Для бота телеграмма нужны id-админов, чтобы он скидывал им информацию об ошибках. Кладём в переменную TELEGRAM_USERS через точку с запятой (получить свой ID можно через различных ботов, например: @getmyid_bot)

**Разворачиваем контейнеры**
 1.  Создаём сеть 
```
	docker network create docker_nw
```
 2. Разворачиваем БД, редис и rabbitmq
```
	cd ./databases && docker-compose up -d --build && cd ..
```
 3. Разворачиваем все остальные сервисы:
```
	cd ./ggl_service && docker-compose up -d --build && cd ..
	cd ./gpt_service && docker-compose up -d --build && cd ..
	cd ./requests_api && docker-compose up -d --build && cd ..
	cd ./telegram_service && docker-compose up -d --build && cd ..
	cd ./tts_service && docker-compose up -d --build && cd ..
	cd ./video_service && docker-compose up -d --build && cd ..
```
