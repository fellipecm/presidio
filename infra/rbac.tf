# RBAC Role Assignments for User

# Storage Blob Data Contributor - for accessing blob storage
resource "azurerm_role_assignment" "user_storage_blob_contributor" {
  scope                = azurerm_storage_account.data.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = var.user_object_id
}

# Storage Queue Data Contributor - for accessing storage queues
resource "azurerm_role_assignment" "user_storage_queue_contributor" {
  scope                = azurerm_storage_account.data.id
  role_definition_name = "Storage Queue Data Contributor"
  principal_id         = var.user_object_id
}

# Storage Account Contributor - for managing storage account
resource "azurerm_role_assignment" "user_storage_account_contributor" {
  scope                = azurerm_storage_account.data.id
  role_definition_name = "Storage Account Contributor"
  principal_id         = var.user_object_id
}

# Website Contributor - for managing Function App
resource "azurerm_role_assignment" "user_function_app_contributor" {
  scope                = azurerm_linux_function_app.python_function_app.id
  role_definition_name = "Website Contributor"
  principal_id         = var.user_object_id
}

# Monitoring Contributor - for Application Insights (conditional)
resource "azurerm_role_assignment" "user_monitoring_contributor" {
  count                = var.enable_application_insights ? 1 : 0
  scope                = azurerm_application_insights.app_insights[0].id
  role_definition_name = "Monitoring Contributor"
  principal_id         = var.user_object_id
}

# Log Analytics Contributor - for Log Analytics workspace (conditional)
resource "azurerm_role_assignment" "user_log_analytics_contributor" {
  count                = var.enable_application_insights ? 1 : 0
  scope                = azurerm_log_analytics_workspace.app_insights_workspace[0].id
  role_definition_name = "Log Analytics Contributor"
  principal_id         = var.user_object_id
}

# Reader role at resource group level for general access
resource "azurerm_role_assignment" "user_resource_group_reader" {
  scope                = data.azurerm_resource_group.personal.id
  role_definition_name = "Reader"
  principal_id         = var.user_object_id
}

# Assign Storage Blob Data Contributor to Function App's managed identity
resource "azurerm_role_assignment" "funcapp_storage_blob_contributor" {
  scope                = azurerm_storage_account.data.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_linux_function_app.python_function_app.identity[0].principal_id

  depends_on = [azurerm_linux_function_app.python_function_app]
}

# Assign Storage Queue Data Contributor to Function App's managed identity
resource "azurerm_role_assignment" "funcapp_storage_queue_contributor" {
  scope                = azurerm_storage_account.data.id
  role_definition_name = "Storage Queue Data Contributor"
  principal_id         = azurerm_linux_function_app.python_function_app.identity[0].principal_id

  depends_on = [azurerm_linux_function_app.python_function_app]
}
