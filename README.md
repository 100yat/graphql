Как развернуть проект локально? (через CLI на Ubuntu / WSL)

Установить проект и управлять зависимостями в нем помогает менеджер пакетов poetry.

Установка poetry: https://python-poetry.org/docs/#installation

У вас есть аккаунт на Github + настроенная связь с удаленным репозиторием по SSH:
https://docs.github.com/en/authentication/connecting-to-github-with-ssh
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Клонирование репозитория.
На странице репозитория https://github.com/yatledger/graphql делаем fork. 
Убрать галочку Copy the master branch only.

На странице репозитория в СВОЕМ аккаунте на Github - <> Code - Копируем SSH - 
$ git clone <SSH>

Установка Docker и Docker Compose: 
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04

Перейдите в каталог проекта с помощью команды cd <путь_к_каталогу_проекта>.

Создание виртуального окружения с именем env в текущем каталоге с помощью venv:
$ python3 -m venv env

Активация виртуального окружения:
$ source env/bin/activate

Установка зависимостей с помощью Poetry:
$ poetry install

Запуск проекта с помощью Docker Compose:
$ docker-compose up -d

Проверка работы контейнеров - в новом окне терминала.
Чтобы посмотреть список всех запущенных контейнеров и их статусы, нужно открыть другое окно терминала и выполнить следующую команду в директории graphql:
$ docker-compose ps

Если статус контейнера State отображается как "Up" и время работы указано, как x минут, это означает, 
что контейнер успешно запущен и работает с момента его запуска.

Вы также можете использовать встроенные инструменты мониторинга Docker, 
чтобы проверить нагрузку на ваши контейнеры и ресурсы, которые они используют:
$ docker stats

Чтобы отслеживать логи каждого контейнера и увидеть, что происходит внутри них:
 $ docker-compose logs <название_контейнера> 

Например:
$ docker-compose logs mongodb
$ docker-compose logs rabbitmq
$ docker-compose logs redis

Проверка через браузер. Посмотрите содержимое файла docker-compose.yaml. 
Там указаны номера портов для каждого сервиса (контейнера). В браузере:

http://localhost:<порт>
Или
http://localhost:<порт>/<хост сервиса>, 

Например: 
http://localhost:5672/rabbit
http://localhost:15672/rabbit
http://localhost:27017/mongo
http://localhost:6379/redis

Остановка контейнеров и выход из виртуального окружения:
Остановка контейнеров: Перейдите в окно терминала, в котором запущен процесс docker-compose up. 
Нажмите Ctrl + C в терминале.

Выход из виртуального окружения:
$ deactivate

