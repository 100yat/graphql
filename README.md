Как развернуть проект локально? (через CLI на Ubuntu / WSL)

Установить проект и управлять зависимостями в нем помогает менеджер пакетов poetry.
1. Установка poetry: https://python-poetry.org/docs/#installation
2. У вас есть аккаунт на Github + настроенная связь с удаленным репозиторием по SSH:
  https://docs.github.com/en/authentication/connecting-to-github-with-ssh
  https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent
3. Клонирование репозитория. На странице репозитория https://github.com/yatledger/graphql делаем fork.
Убрать галочку Copy the master branch only, потому что потом для локальной разработки нужно будет сделать ветку от ветки develop.
4. На странице репозитория в СВОЕМ аккаунте на Github - <> Code - Копируем SSH - 
  $ git clone <SSH>
5. Установка Docker и Docker Compose: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04
6. Перейдите в каталог проекта с помощью команды cd <путь_к_каталогу_проекта>.
7. Создание виртуального окружения с именем env в текущем каталоге с помощью venv:
  $ python3 -m venv env
8. Активация виртуального окружения:
$ source env/bin/activate
9. Установка зависимостей с помощью Poetry:
$ poetry install
10. Запуск проекта с помощью Docker Compose:
$ docker-compose up -d

Проверка работы контейнеров - в новом окне терминала.
11. Чтобы посмотреть список всех запущенных контейнеров и их статусы, нужно открыть другое окно терминала и выполнить следующую команду в директории graphql:
  $ docker-compose ps
Если статус контейнера State отображается как "Up" и время работы указано, как x минут, это означает, что контейнер успешно запущен и работает с момента его запуска.
12. Вы также можете использовать встроенные инструменты мониторинга Docker, чтобы проверить нагрузку на ваши контейнеры и ресурсы, которые они используют:
  $ docker stats

13. Чтобы отслеживать логи каждого контейнера и увидеть, что происходит внутри них. 
  $ docker-compose logs <название_контейнера> 
Например:
  $ docker-compose logs mongodb
  $ docker-compose logs rabbitmq
  $ docker-compose logs redis
14. Проверка через браузер. Посмотрите содержимое файла docker-compose.yaml. 
Там указаны номера портов для каждого сервиса (контейнера). В браузере:
http://localhost:<порт>
Или
http://localhost:<порт>/<хост сервиса>, 

Например: 
http://localhost:5672/rabbit
http://localhost:15672/rabbit
http://localhost:27017/mongo
http://localhost:6379/redis

15. Остановка контейнеров и выход из виртуального окружения.
Остановка контейнеров: Перейдите в окно терминала, в котором запущен процесс docker-compose up. 
Нажмите Ctrl + C в терминале.

16. Выход из виртуального окружения:
  $ deactivate

