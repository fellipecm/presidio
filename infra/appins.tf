# Create Log Analytics Workspace for Application Insights (conditional)
resource "azurerm_log_analytics_workspace" "app_insights_workspace" {
  count               = var.enable_application_insights ? 1 : 0
  name                = "${var.project_name}-law"
  resource_group_name = data.azurerm_resource_group.personal.name
  location            = var.location
  sku                 = "PerGB2018"
  retention_in_days   = 30

  tags = var.tags
}

# Create Application Insights (conditional)
resource "azurerm_application_insights" "app_insights" {
  count               = var.enable_application_insights ? 1 : 0
  name                = "${var.project_name}-ai"
  resource_group_name = data.azurerm_resource_group.personal.name
  location            = var.location
  workspace_id        = azurerm_log_analytics_workspace.app_insights_workspace[0].id
  application_type    = "web"

  tags = var.tags
}
