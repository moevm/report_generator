# Инструкция 

**Создать гитхаб бота**

1. в папке src создать файл `oauth.txt` с токеном для гитхаба
1. в папке src создать файл `github_data.txt`
```
<client_ID>
<client_secret>
```
3. `./build_and_run_docker.sh`
4. Зайти в докер: `docker exec -it report_generator_doc bash`
5. Вставить в файл `/var/www/.ssh/id_rsa` ssh ключ
6. `bash /report_generator/scripts/init.sh` + согласиться на добавление know_hosts
7. Уже на вашей машине в `/etc/hosts` прописать `127.0.0.1      report-generator`
8. Перейти на `report-generator:8077`
