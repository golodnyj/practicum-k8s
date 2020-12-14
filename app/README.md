# TodoList — демо-приложение для вебинара

Как подготовить приложение для запуска в Яндекс.Облаке:
1. Аутентифицироваться в Container Registry
```
yc container registry configure-docker
```

1. Создать Container Registry
```
yc container registry create --name todo-registry
```

1. Собрать docker-образ с тегом v1
```
sudo docker build . --tag cr.yandex/<registry_id>/todo-demo:v1
```

1. Собрать docker-образ с тегом v2 (для проверки сценария обновления приложения)
```
sudo docker build . --build-arg COLOR_SCHEME=dark --tag cr.yandex/<registry_id>/todo-demo:v2
```

1. Загрузить docker-образы в Container Registry
```
sudo docker push cr.yandex/<registry_id>/todo-demo:v1
sudo docker push cr.yandex/<registry_id>/todo-demo:v2
```
