# report_generator
## Настройка и активация виртуального окружения

1. Необходимо установить:

* `sudo apt install python3.6`

* `sudo apt-get install python3.6-venv`

2. После необходимое сгенерировать папку:

* `python3.6 -m venv venv`

3. Для активации виртуального окружения:

* Для активации: `source venv/bin/activate` (для linux'a)

4. Установка зависимостей:

* `pip3.6 install -r requirements.txt`

5. Для деактивации виртуального окружения: `deactivate`

6. Если вы не стали активировать виртуальное окружение, то для установки зависимостей:
`./venv/bin/pip3.6 install -r requirements.txt `
Если Вы хотите явно указать какой python используете, то в дальнейшем писать надо так:`venv/bin/python3.6 main.py`


## Инструкция.
 Для того, чтобы программа работала корректно, установите unoconv
```
sudo apt-get install unoconv
```
 Для запуска введем:
```
./main.py
```
### Пример запуска программы.
# Ввод входных данных вручную
```
./main.py
url_of_repo(ssh):ссылка на ваш репозиторий
wiki_repo(https):ccылка на wiki странички
branch: ветка, на которой появится отчет на основе wiki
```
# Ввод входнных данных из файла
```
./main.py -f <файл с информацией о репозитории, вики и ветке>
```
В файле порядок входных параметров должен быть таким же как при вводе входных данных вручную.

В результате в указанном репозитории на указанной ветке появиться отчет, соответствующий настройкам, находящиxся в settings.json.
