# Data source to get existing personal resource group
data "azurerm_resource_group" "personal" {
  name = var.resource_group_name
}