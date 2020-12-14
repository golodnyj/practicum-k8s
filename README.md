# Практикум: развертывание отказоустойчивого приложения в Managed Service for Kubernetes® и MDB

# Требуемое окружение

В рамках практической работы окружение подготовлено в виде образа ВМ. Из этого образа будет создана виртуальная машина,
на которой и будет выполняться работа. Для самостоятельного выполнения работы придется настроить окружение самостоятельно.

Для выполнения практической работы:
1. Установите следующие утилиты:
* yc (https://cloud.yandex.ru/docs/cli/quickstart);
* Terraform (https://learn.hashicorp.com/tutorials/terraform/install-cli);
* Docker (https://docs.docker.com/get-docker/);
* Kubectl (https://kubernetes.io/docs/tasks/tools/install-kubectl/);
* envsubst;
* git;
* ssh;
* curl.

2. Зарегистрироваться в Яндекс.Облаке (https://cloud.yandex.ru/);
3. Добавить в облако каталог, в котором будете создавать ресурсы. 

# Подготовка окружения
## Шаг 0. Вход в облако
Видео: https://youtu.be/M0fXvr8h8bE  
* Проверяем предсозданные ресурсы в облаке.

## Шаг 1. Создание VM + Настройка консольной утилиты yc
Видео: https://youtu.be/_jKRNy0SJ5E
* Настраиваем доступ по протоколу SSH.  
* Настраиваем консольную утилиту yc.  

### Настройка доступа по протоколу SSH
1. Убедитесь, что у вас есть SSH-ключ или сгенерируйте новый (подробная [инструкция](https://cloud.yandex.ru/docs/compute/operations/vm-connect/ssh#creating-ssh-keys)).
```
ssh-keygen -t rsa -b 2048 # генерация нового ssh-ключа
cat ~/.ssh/id_rsa.pub
```

2. Создайте в Консоли виртуальную машину из образа `base-image`:
* В каталоге нажмите кнопку `Создать ресурс`, выберите ресурс `Виртуальная машина`, введите имя `lab-vm`.
* В секции `Выбор образа/загрузочного диска` выберете вкладку `Пользовательские`, выберете загрузочный диск
из образа `base-image`.
* В секции `Диски` у созданного диска выберите `Тип диска` SSD.
* В разделе `Доступ` выберите аккаунт `sa-admin-<folder-id>`, введите логин для входа на ВМ.
Скопируйте SSH-ключ из файла `~/.ssh/id_rsa.pub`.

3. Дождитесь создания ВМ (статуса `Running`);
4. Зайдите на страницу ВМ, убедитесь что привязан сервисный аккаунт `sa-admin-<folder-id>`, скопируйте публичный IPv4 адрес;
5. Войдите на созданную ВМ по SSH;
6. Дальнейшие команды выполняйте на созданной ВМ.

### Настройка консольной утилиты yc для работы с Яндекс Облаком
1. В браузере вернитесь на страницу облака и скопируйте id каталога:
```
echo "export FOLDER_ID=folder-id-here" >> ~/.bashrc && . ~/.bashrc
echo $FOLDER_ID
```
3. Выполните в терминале команду `yc config set folder-id $FOLDER_ID`;
2. Выполните в терминале команду `yc config set instance-service-account true`, чтобы использовать yc от привязанного к ВМ
сервисного аккаунта;

4. Чтобы проверить корректность настройки yc, выведите список виртуальных машин в каталоге с помощью команды:
```
yc compute instance list
```

# Развертывание кластера PostgreSQL с помощью Terraform
## Шаг 2. Используем Terraform
Видео: https://youtu.be/ZDYVsVMuZeQ
* Знакомимся с конфигурацией Terraform
* Инициализация Terraform и создание кластера PostgreSQL


### Спецификация Terraform

1. На ВМ загружен репозиторий с файлами для практической работы. Обновите версию репозитория и сохраните 
путь к репозиторию в переменной окружения `REPO`:
```
echo "export REPO=/home/common/yandex-scale-2020-lab-k8s" >> ~/.bashrc && . ~/.bashrc
echo $REPO
cd $REPO
git pull
```

### Инициализация Terraform и создание кластера PostgreSQL

1. Перейдите в каталог с описанием инфраструктуры приложения и инициализируйте Terraform:
```
cd $REPO/terraform/ && ls
terraform init
```
2. Разверните инфраструктуру с помощью Terraform:
```
terraform apply -var yc_folder=$FOLDER_ID -var user=$USER
```

3. На время развертывания кластера оставьте открытым терминал с запущенным Terraform
и перейдите к следующему шагу. Позже мы проверим, что кластер создался.

# Обзор кластера Managed K8S и создание группы узлов
## Шаг 3. Создаем группу узлов
Видео: https://youtu.be/PfjaBv7X4o8
* Обзор созданного кластера
* Создание группы узлов

### Обзор созданного кластера
1. Перейдите в раздел Консоли `Managed Service for Kubernetes`. В нем вы увидете созданный кластер с названием `lab-k8s`.
2. Зайдите на страницу кластера. Обратите внимание на подключенные сервисные аккаунты:
* Сервисный аккаунт `k8s-cluster-manager-<folder-id>` используется для ресурсов, необходимых кластеру.
* Сервисный аккаунт `k8s-image-puller-<folder-id>` используется в качестве сервисного аккаунта для аутентификации
в Container Registry на нодах кластера.
3. Обратите внимание, что создан зональный кластер, а значит создан один экземпляр мастера Kubernetes.

### Создание группы узлов
1. Перейдите на вкладку `Группы узлов` и создайте группу узлов с именем `lab-k8s-group` и одним узлом:
* В разделе `Доступ` введите логин для входа на ВМ. Скопируйте SSH-ключ из файла `~/.ssh/id_rsa.pub`.
2. Пока создается группа узлов, проверьте результаты работы Terraform и подготовьте докер образ с приложением.
Оставьте окно браузера открытым и перейдите в консоль.

# Проверка кластера PostgreSQL
## Шаг 4. Проверяем кластер
Видео: https://youtu.be/NWNnuzBxFD8
* Сохраните переменные
* Проверьте кластер PostgreSQL

### Проверка кластера PostgreSQL
1. Вернитесь к терминалу с запущенным Terraform. По завершении работы в секции `Outputs` отобразятся данные о кластере.

2. Сохраните данные о кластере в переменные окружения:
```
echo "export DATABASE_URI=database_uri-here" >> ~/.bashrc
echo "export DATABASE_HOSTS=database_hosts-here" >> ~/.bashrc
. ~/.bashrc
echo $DATABASE_URI
echo $DATABASE_HOSTS
```

3. Проверьте результат работы Terraform:
```
yc managed-postgresql cluster list
yc managed-postgresql cluster get <ID>
```

# Проверка кластера K8S
## Шаг 5. Проверяем кластер
Видео: https://youtu.be/z_mvuhNOhzw
* Добавить переменные окружения
* Добавить учетные данные

### Добавление переменных окружения
1. На странице браузера, где создавалась группа узлов, проверьте, что создание группы завершено.
2. В терминале проверьте, что кластер доступен к использованию:
```
yc managed-kubernetes cluster list
echo "export K8S_ID=k8s-id-here" >> ~/.bashrc && . ~/.bashrc
echo $K8S_ID
yc managed-kubernetes cluster --id=$K8S_ID get
yc managed-kubernetes cluster --id=$K8S_ID list-node-groups
```

### Добавление учетных данных в конфигурационный файл Kubectl
```
yc managed-kubernetes cluster get-credentials --id=$K8S_ID --external
```
Конфигурация будет записана в файл `~/.kube/config`, проверим его содержимое:
```
cat ~/.kube/config
```

# Подготовка Docker-образов
## Шаг 6. Работаем с Docker
Видео: https://youtu.be/dArqkeLksQk
* Создать Container Registry
* Собрать Docker-образ

### Создание Container Registry
1. Создайте реестр: `yc container registry create --name lab-registry`;
2. Сохраните id реестра:
```
echo "export REGISTRY_ID=registry-id-here" >> ~/.bashrc && . ~/.bashrc
```
2. Проверьте наличие реестра через терминал:
```
yc container registry list
yc container registry get $REGISTRY_ID
```

3. Настройте аутентификацию в docker:
```
yc container registry configure-docker
cat ~/.docker/config.json
```
Файл `config.json` содержит вашу конфигурацию после авторизации:
```
{
  "credHelpers": {
    "container-registry.cloud.yandex.net": "yc",
    "cr.cloud.yandex.net": "yc",
    "cr.yandex": "yc"
  }
}
```

### Сборка и загрузка Docker-образов в Container Registry
1. Перейдите к исходникам приложения:
```
cd $REPO/app && ls
```

2. Соберите образ приложения:
```
sudo docker build . --tag cr.yandex/$REGISTRY_ID/lab-demo:v1
sudo docker images
```

3. Загрузите образ
```
sudo docker push cr.yandex/$REGISTRY_ID/lab-demo:v1
```

### Просмотр списка Docker-образов

1. Получите список Docker-образов в реестре командой `yc container image list`.
* В результате в таблице отборазятся ID образа, дата его создания и другие данные.

# Развертывание приложения и балансировщика нагрузки в k8s
## Шаг 7. Работаем с kubectl
Видео: https://youtu.be/q5NR5wJwPpQ

1. Просмотрите файлы конфигурации:
```
cd $REPO/k8s-files && ls
cat lab-demo.yaml.tpl
cat load-balancer.yaml
```

2. В файле `lab-demo.yaml.tpl` замените значение переменных:
* Переменные `DATABASE_URI` и `DATABASE_HOSTS` получены в результате работы terraform на четвертом шаге.
* `REGISTRY_ID` получали ранее с помощью команды `yc container registry list`.
```
envsubst \$REGISTRY_ID,\$DATABASE_URI,\$DATABASE_HOSTS <lab-demo.yaml.tpl > lab-demo.yaml
cat lab-demo.yaml
```

3. Убедитесь что все переменные окружения из файла `lab-demo.yaml.tpl` заменились на реальные значения
в файле `lab-demo.yaml`

4. Разверните ресурсы:
```
kubectl apply -f lab-demo.yaml
kubectl describe deployment lab-demo
```

```
kubectl apply -f load-balancer.yaml
kubectl describe service lab-demo
```

5. Как только балансировщик нагрузки полноценно развернется и получит внешний URL (поле `LoadBalancer Ingress`),
проверим работоспособность сервиса в браузере.

# Изменения в архитектуре сервиса для обеспечения отказоустойчивости
## Шаг 8. Изменения в архитектуре сервиса
Видео: https://youtu.be/c9yXNJPfeuo

После выполнения всех шагов имеем:
* MDB PostgreSQL с одним хостом.
* Managed Kubernetes с зональным мастером (1 хост) и группой узлов из одного узла.
* одну реплику приложения, запущенную в k8s.

### Отказоустойчивый MDB PostgreSQL

В MDB можно увеличить количество хостов в кластере без остановки работы.
1. Перейдите во вкладку `Managed Service for PostgreSQL` в UI, выберите созданный кластер, во вкладке `Хосты` добавьте хост.
2. Выберите зону доступности, отличную от той, которая используется для первого хоста.
3. Убедитесь, что у хостов в кластере достаточно ресурсов, чтобы обрабатывать возвросшую нагрузку при отказе одного
или нескольких хостов.

### Отказоустойчивый Managed Kubernetes

Необходимо создать региональный мастер, состоящий из трех хостов. Тип мастера уже созданного кластера
поменять нельзя, поэтому придется создать новый кластер.
1. Перейдите во вкладку `Managed Service for Kubernetes` и создайте новый кластер.
2. Выберите тип мастера `Региональный`.
3. Создайте группу узлов с тремя узлами.
4. Убедитесь, что у хостов в группе узлов достаточно ресурсов, чтобы обрабатывать возвросшую нагрузку при отказе одного
или нескольких хостов.

### Отказоустойчивое приложение

При развертывании приложения в k8s вы указывали одну реплику, теперь надо увеличить количество реплик до трех. Созданный
балансировщик нагрузки будет распределять нагрузку по всем трем репликам.

# Удаление ресурсов
## Шаг 9. Удаление ресурсов
Видео: https://youtu.be/CaDWyC0Mpvo
* Удаление ресурсов из кластера k8s.  
* Удаление кластера k8s.  
* Удаление базы данных в Terraform.  
* Удаление реестра и Docker-образов.  
* Удаление ВМ с настроенным окружением.  

### Удаление ресурсов из кластера k8s
```
kubectl delete -f load-balancer.yaml
kubectl delete -f lab-demo.yaml
```

### Удаление кластера k8s
```
yc managed-kubernetes cluster list
yc managed-kubernetes cluster delete lab-k8s
yc managed-kubernetes cluster list
```

### Удаление базы данных в Terraform
```
cd $REPO/terraform
terraform destroy -var yc_folder=$FOLDER_ID -var user=$USER
yc managed-postgresql cluster list
```

### Удаление реестра и Docker-образов
Перейдите во вкладку `Container Registry` в Консоли, выберите реестр `lab-registry` и удалите в нем все образы.
После этого вернитесь к списку реестров, нажмите раскрывающееся меню для реестра `lab-registry` и удалите реестр.

### Удаление ВМ с настроенным окружением 
В консоли перейдите во вкладку `Compute`, нажмите раскрывающееся меню для ВМ `lab-vm` и удалите эту ВМ.