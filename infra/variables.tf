# Resource Group Name
variable "resource_group_name" {
  description = "Name of the existing personal resource group"
  type        = string
  default     = "personal"
}

# Location
variable "location" {
  description = "Azure region where resources will be created"
  type        = string
  default     = "Australia East"
}

# Project Name
variable "project_name" {
  description = "Name of the project (used as prefix for resources)"
  type        = string
  default     = "presidio"
}

# App Service Plan SKU
variable "app_service_plan_sku" {
  description = "The SKU for the App Service Plan"
  type        = string
  default     = "B1"
  
  validation {
    condition = contains([
      "B1", "B2", "B3",           # Basic
      "S1", "S2", "S3",           # Standard
      "P1v2", "P2v2", "P3v2",     # Premium v2
      "P1v3", "P2v3", "P3v3"      # Premium v3
    ], var.app_service_plan_sku)
    error_message = "The app_service_plan_sku must be a valid Azure App Service Plan SKU."
  }
}

# Tags
variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default = {
    Environment = "development"
    Project     = "presidio"
    Owner       = "personal"
  }
}

# Python Version for Function App
variable "python_version" {
  description = "Python version for the Function App"
  type        = string
  default     = "3.12"
  
  validation {
    condition = contains([
      "3.9", "3.10", "3.11", "3.12"
    ], var.python_version)
    error_message = "The python_version must be a supported Azure Functions Python version (3.9, 3.10, 3.11, 3.12)."
  }
}

# Application Insights Enable/Disable
variable "enable_application_insights" {
  description = "Enable Application Insights for monitoring (requires appropriate permissions)"
  type        = bool
  default     = true
}

# User Object ID for RBAC assignments
variable "user_object_id" {
  description = "Object ID of the user to grant permissions to"
  type        = string
  default     = "2ccda7b1-5a78-4960-a4e5-f6eacff39c1e"
}
