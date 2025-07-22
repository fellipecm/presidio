# Resource Group Information
output "resource_group_name" {
  description = "Name of the resource group"
  value       = data.azurerm_resource_group.personal.name
}

output "resource_group_location" {
  description = "Location of the resource group"
  value       = data.azurerm_resource_group.personal.location
}

# App Service Plan Information
output "app_service_plan_id" {
  description = "ID of the App Service Plan"
  value       = azurerm_service_plan.app_service_plan.id
}

output "app_service_plan_name" {
  description = "Name of the App Service Plan"
  value       = azurerm_service_plan.app_service_plan.name
}

# Storage Account Information
output "storage_account_name" {
  description = "Name of the storage account"
  value       = azurerm_storage_account.data.name
}

output "storage_account_primary_key" {
  description = "Primary access key for the storage account"
  value       = azurerm_storage_account.data.primary_access_key
  sensitive   = true
}

output "storage_account_connection_string" {
  description = "Connection string for the storage account"
  value       = azurerm_storage_account.data.primary_connection_string
  sensitive   = true
}

output "storage_container_name" {
  description = "Name of the data storage container"
  value       = azurerm_storage_container.data.name
}

# Storage Queue Information
output "pii_processing_queue_name" {
  description = "Name of the PII processing queue"
  value       = azurerm_storage_queue.pii_processing.name
}

output "pii_results_queue_name" {
  description = "Name of the PII results queue"
  value       = azurerm_storage_queue.pii_results.name
}

output "storage_queue_endpoint" {
  description = "Storage account queue service endpoint"
  value       = azurerm_storage_account.data.primary_queue_endpoint
}

# Function App Information
output "function_app_name" {
  description = "Name of the Function App"
  value       = azurerm_linux_function_app.python_function_app.name
}

output "function_app_default_hostname" {
  description = "Default hostname of the Function App"
  value       = azurerm_linux_function_app.python_function_app.default_hostname
}

output "function_app_url" {
  description = "URL of the Function App"
  value       = "https://${azurerm_linux_function_app.python_function_app.default_hostname}"
}

# Application Insights Information (conditional)
output "application_insights_name" {
  description = "Name of the Application Insights instance"
  value       = var.enable_application_insights ? azurerm_application_insights.app_insights[0].name : "Application Insights disabled"
}

output "application_insights_instrumentation_key" {
  description = "Instrumentation key for Application Insights"
  value       = var.enable_application_insights ? azurerm_application_insights.app_insights[0].instrumentation_key : "Not available"
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Connection string for Application Insights"
  value       = var.enable_application_insights ? azurerm_application_insights.app_insights[0].connection_string : "Not available"
  sensitive   = true
}

output "application_insights_app_id" {
  description = "Application ID for Application Insights"
  value       = var.enable_application_insights ? azurerm_application_insights.app_insights[0].app_id : "Not available"
}

output "log_analytics_workspace_id" {
  description = "ID of the Log Analytics Workspace"
  value       = var.enable_application_insights ? azurerm_log_analytics_workspace.app_insights_workspace[0].id : "Not available"
}

output "log_analytics_workspace_name" {
  description = "Name of the Log Analytics Workspace"
  value       = var.enable_application_insights ? azurerm_log_analytics_workspace.app_insights_workspace[0].name : "Not available"
}

# RBAC Assignment Information
output "rbac_assignments" {
  description = "RBAC role assignments created for the user"
  value = {
    storage_blob_contributor     = azurerm_role_assignment.user_storage_blob_contributor.id
    storage_queue_contributor    = azurerm_role_assignment.user_storage_queue_contributor.id
    storage_account_contributor  = azurerm_role_assignment.user_storage_account_contributor.id
    function_app_contributor     = azurerm_role_assignment.user_function_app_contributor.id
    resource_group_reader        = azurerm_role_assignment.user_resource_group_reader.id
    monitoring_contributor       = var.enable_application_insights ? azurerm_role_assignment.user_monitoring_contributor[0].id : "Not applicable"
    log_analytics_contributor    = var.enable_application_insights ? azurerm_role_assignment.user_log_analytics_contributor[0].id : "Not applicable"
  }
}

output "user_permissions_summary" {
  description = "Summary of permissions granted to the user"
  value = {
    user_object_id = var.user_object_id
    permissions = [
      "Storage Blob Data Contributor - Read/write access to blob storage",
      "Storage Queue Data Contributor - Read/write access to storage queues", 
      "Storage Account Contributor - Manage storage account settings",
      "Website Contributor - Manage Function App",
      "Reader - Read access to resource group",
      var.enable_application_insights ? "Monitoring Contributor - Manage Application Insights" : "Application Insights - Not enabled",
      var.enable_application_insights ? "Log Analytics Contributor - Manage Log Analytics workspace" : "Log Analytics - Not enabled"
    ]
  }
}
