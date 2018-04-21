# Ближайшие бары

Данный скрипт позволяет определить:

* самый большой бар
* самый маленький бар
* самый ближайший бар

на основании данных, опубликованных на [Портале открытых данных Правительства Москвы](http://data.mos.ru/)

# Как запустить

Перед запуском скрипта необходимо скачать файл в формате JSON с исходными данными о барах. Для этого необходимо:

1. [Зарегистрироваться](https://apidata.mos.ru/Account/Register) на сайте apidata.mos.ru для получения API ключа
2. Скачать JSON файл по ссылке 

Скрипт требует для своей работы установленного интерпретатора Python версии 3.5

Запуск на Linux:

```bash

$ python3 bars.py bars.json 55.62146 37.41241

--------------------
Самый большой бар:
--------------------
Название:  СуперБольшойБар
Количество мест:  258
Административный округ:  Южный административный округ
Район:  Даниловский район
Адрес:  Уличная улица, дом 1
Телефон:  (123) 123-45-67
Координаты: 12.34 с.ш.  34.56 в.д.

--------------------
Самый маленький бар:
--------------------
Название:  СамыйМаленькийБар
Количество мест:  0
Административный округ:  Северный административный округ
Район:  район Коптево
Адрес:  Переуличный переулок, дом 2
Телефон:  (123) 987-65-43
Координаты: 43.21 с.ш.  65.43 в.д.

--------------------
Самый ближайший бар:
--------------------
Название:  СамыйБлижайшийБар
Количество мест:  10
Административный округ:  Новомосковский административный округ
Район:  поселение Московский
Адрес:  Бульварный бульвар, дом 3
Телефон:  (123) 765-43-21
Координаты: 55.55 с.ш.  37.37 в.д.

```

Запуск на Windows происходит аналогично.

# Цели проекта

Код создан в учебных целях. В рамках учебного курса по веб-разработке - [DEVMAN.org](https://devman.org)
