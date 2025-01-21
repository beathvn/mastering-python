# https://developer.hashicorp.com/terraform/tutorials/configuration-language/versions
terraform {
  required_providers {
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 3.1.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.16.0"
    }
  }
  required_version = ">= 1.10.4"
}
