terraform {
  required_providers {
    yandex = {
      source = "terraform-providers/yandex"
    }
  }
}

provider "yandex" {
  endpoint =  "api.cloud.yandex.net:443"
  folder_id = var.yc_folder
}
