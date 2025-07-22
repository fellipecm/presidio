# Create a Storage Account called "data"
resource "azurerm_storage_account" "data" {
  name                     = "${var.project_name}data${random_string.storage_suffix.result}"
  resource_group_name      = data.azurerm_resource_group.personal.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  # Enable queue service
  queue_properties {
    logging {
      delete                = true
      read                  = true
      write                 = true
      version               = "1.0"
      retention_policy_days = 10
    }
    
    minute_metrics {
      enabled               = true
      version               = "1.0"
      include_apis          = true
      retention_policy_days = 10
    }
    
    hour_metrics {
      enabled               = true
      version               = "1.0"
      include_apis          = true
      retention_policy_days = 10
    }
  }

  tags = var.tags
}

# Random string for storage account name uniqueness
resource "random_string" "storage_suffix" {
  length  = 6
  special = false
  upper   = false
}

# Create a storage container called "data"
resource "azurerm_storage_container" "data" {
  name                  = "data"
  storage_account_name  = azurerm_storage_account.data.name
  container_access_type = "private"
}

# Create a storage queue for PII processing
resource "azurerm_storage_queue" "pii_processing" {
  name                 = "pii-processing"
  storage_account_name = azurerm_storage_account.data.name
}

# Create a storage queue for PII results
resource "azurerm_storage_queue" "pii_results" {
  name                 = "pii-results"
  storage_account_name = azurerm_storage_account.data.name
}
