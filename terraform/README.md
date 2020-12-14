# Terraform-спецификация окружения для TodoList

## Деплой приложения
1. Установить terraform: `https://www.terraform.io`
1. Инициализировать terraform в директории со спецификацией:
    ```
    terraform init
    ```
1. Если реестр, в котором лежат docker-образы приложения, называется не `registry-lab`, измените переменную `registry_name` 
в файле [main.tf](main.tf).
1. Развернуть и запустить приложение. 
    * folder_id - каталог, в котором будет развернуто приложение,
    * yc_token - OAuth токен пользователя, от имени которого будет развернуто приложение
    ```
    terraform apply -var yc_folder=<folder_id> -var yc_token=<yc_token> -var user=$USER
    ```

## Создаваемые ресурсы
* VPC Network с тремя подсетями во всех зонах доступности;
* Кластер Managed PostgreSQL с одним хостом в зоне доступности `ru-central1-a`;

## Удаление приложения
```
terraform destroy -var yc_folder=<folder_id> -var yc_token=<yc_token> -var user=$USER
```
