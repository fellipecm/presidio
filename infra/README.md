# Presidio Infrastructure

This Terraform configuration deploys Azure resources for the Presidio project in your personal resource group.

## Resources Created

1. **App Service Plan** - Linux-based hosting plan for applications
2. **Function App** - Azure Functions with Python 3.12 runtime
3. **Storage Account** - Named "data" (with unique suffix) for application storage

## Prerequisites

- Azure CLI installed and authenticated
- Terraform installed (version >= 1.0)
- An existing Azure resource group (personal)

## Usage

1. **Initialize Terraform**
   ```bash
   terraform init
   ```

2. **Create terraform.tfvars file**
   ```bash
   cp terraform.tfvars.example terraform.tfvars
   ```
   
   Edit `terraform.tfvars` and update the values:
   - `resource_group_name`: Name of your existing personal resource group
   - `project_name`: Prefix for resource names
   - `app_service_plan_sku`: SKU for the App Service Plan (B1, S1, P1v2, etc.)

3. **Plan the deployment**
   ```bash
   terraform plan
   ```

4. **Apply the configuration**
   ```bash
   terraform apply
   ```

## Configuration Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `resource_group_name` | Name of existing resource group | `personal` | Yes |
| `project_name` | Project name (resource prefix) | `presidio` | No |
| `app_service_plan_sku` | App Service Plan SKU | `B1` | No |
| `tags` | Resource tags | See variables.tf | No |

## Outputs

After deployment, the following outputs will be available:
- Resource group information
- App Service Plan details
- Storage account connection details (sensitive)
- Function App URL and hostname

## Resource Naming Convention

- App Service Plan: `{project_name}-asp`
- Function App: `{project_name}-func`
- Storage Account: `{project_name}data{random_suffix}`

## Clean Up

To destroy the created resources:
```bash
terraform destroy
```
