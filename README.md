# report_generator
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
```
./main.py
url_of_repo(ssh):ссылка на ваш репозиторуй
wiki_repo(https):ccылка на wiki странички
branch: ветка, на которой появиться отчет на основе wiki
```
В результате на указанном репозитории на указанной ветке появиться отчет, соответствующий настройкам, находящиxся в settings.json.
