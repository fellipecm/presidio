# Create an App Service Plan with Linux VMs
resource "azurerm_service_plan" "app_service_plan" {
  name                = "${var.project_name}-asp"
  resource_group_name = data.azurerm_resource_group.personal.name
  location            = var.location
  os_type             = "Linux"
  sku_name            = var.app_service_plan_sku

  tags = var.tags
}

# Create a Function App with Python 3.12 runtime
resource "azurerm_linux_function_app" "python_function_app" {
  name                = "${var.project_name}-func"
  resource_group_name = data.azurerm_resource_group.personal.name
  location            = var.location

  storage_account_name       = azurerm_storage_account.data.name
  storage_account_access_key = azurerm_storage_account.data.primary_access_key
  service_plan_id            = azurerm_service_plan.app_service_plan.id

  identity {
    type = "SystemAssigned"
  }

  site_config {
    always_on = true
    
    application_stack {
      python_version = var.python_version
    }

    # Enable CORS if needed
    cors {
      allowed_origins = ["*"]
    }
  }

  app_settings = merge({
    "FUNCTIONS_WORKER_RUNTIME"       = "python"
    "WEBSITE_RUN_FROM_PACKAGE"       = "1"
    "PYTHON_VERSION"                 = var.python_version
    "STORAGE_ACCOUNT_NAME"           = azurerm_storage_account.data.name
    "STORAGE_ACCOUNT_KEY"            = azurerm_storage_account.data.primary_access_key
    "STORAGE_CONNECTION_STRING"      = azurerm_storage_account.data.primary_connection_string
    "PII_PROCESSING_QUEUE_NAME"      = azurerm_storage_queue.pii_processing.name
    "PII_RESULTS_QUEUE_NAME"         = azurerm_storage_queue.pii_results.name
    "STORAGE_CONTAINER_NAME"         = azurerm_storage_container.data.name
    "PRESIDIO_LOG_LEVEL"             = "INFO"
    # SCM settings for Azure deployment
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
    "ENABLE_ORYX_BUILD"              = "true"
    # Python specific settings
    "PYTHON_ENABLE_GUNICORN_MULTIPROCESSING" = "true"
    # Enhanced monitoring and logging
    "FUNCTIONS_EXTENSION_VERSION"    = "~4"
    "AzureFunctionsJobHost__logging__logLevel__default" = "Information"
  }, var.enable_application_insights ? {
    # Application Insights configuration (conditional)
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.app_insights[0].instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.app_insights[0].connection_string
    "ApplicationInsightsAgent_EXTENSION_VERSION" = "~3"
    "XDT_MicrosoftApplicationInsights_Mode"      = "Recommended"
    "APPINSIGHTS_PROFILERFEATURE_VERSION"       = "1.0.0"
    "APPINSIGHTS_SNAPSHOTFEATURE_VERSION"       = "1.0.0"
    "InstrumentationEngine_EXTENSION_VERSION"   = "~1"
    "SnapshotDebugger_EXTENSION_VERSION"        = "~1"
    "XDT_MicrosoftApplicationInsights_BaseExtensions" = "~1"
    "AzureFunctionsJobHost__logging__applicationInsights__samplingSettings__isEnabled" = "true"
  } : {})

  tags = var.tags
}
