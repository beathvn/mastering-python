locals {
  namespace = "my-namespace"
}

terraform {
  backend "azurerm" {
    container_name = "terraform"
    snapshot       = true
    # as parameters or env variables please provide: access_key, storage_account_name, key
    # https://www.terraform.io/docs/backends/types/azurerm.html
  }
}

provider "azurerm" {
  features {}
  resource_provider_registrations = "none"
}

# 'data' connects to something else (other file...)
data "azurerm_client_config" "current" {}

data "azurerm_resource_group" "main" {
  name = "rg-${local.namespace}-${var.environment}-${var.region}-01"
}
