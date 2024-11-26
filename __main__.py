"""An Azure RM Python Pulumi program"""

import os
import pulumi
from pulumi import Output, FileAsset
from pulumi_azure_native import storage, resources, insights, web

# Create an Azure Resource Group
resource_group = resources.ResourceGroup(
    'resourceGroup',
    location="westeurope"
)

# Create a Storage Account
storage_account = storage.StorageAccount('storageaccount',
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(
        name=storage.SkuName.STANDARD_LRS,
    ),
    kind=storage.Kind.STORAGE_V2,
    allow_blob_public_access=True
)

# Get storage account keys (needed for Blob upload)
storage_account_keys = storage.list_storage_account_keys_output(
    resource_group_name=resource_group.name,
    account_name=storage_account.name
)
primary_storage_key = storage_account_keys.keys[0].value

# Create a Blob Container
zip_container = storage.BlobContainer('zipcontainer',
    account_name=storage_account.name,
    resource_group_name=resource_group.name,
    public_access=storage.PublicAccess.BLOB
)

# Upload the zip file to Blob Storage
app_zip_path = os.path.join(os.getcwd(), 'hello_world.zip')

app_zip_blob = storage.Blob('appzip',
    resource_group_name=resource_group.name,
    account_name=storage_account.name,
    container_name=zip_container.name,
    blob_name='hello-world.zip',
    source=FileAsset(app_zip_path),
)

# Construct the Blob URL
blob_url = Output.concat(
    "https://",
    storage_account.name,
    ".blob.core.windows.net/",
    zip_container.name,
    "/",
    app_zip_blob.name
)

# Create Application Insights
app_insights = insights.Component('appInsights',
    resource_group_name=resource_group.name,
    kind='web',
    application_type='web',
    ingestion_mode="ApplicationInsights"
)

# Create an App Service Plan (Free tier)
app_service_plan = web.AppServicePlan('appServicePlan',
    resource_group_name=resource_group.name,
    reserved=True,
    kind='Linux',
    sku=web.SkuDescriptionArgs(
        name='F1',
        tier='Free'
    )
)

# Create a Web App
app = web.WebApp('webApp',
    resource_group_name=resource_group.name,
    server_farm_id=app_service_plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[
            web.NameValuePairArgs(
                name='WEBSITE_RUN_FROM_PACKAGE',
                value=blob_url
            ),
        ],
        linux_fx_version='PYTHON|3.9',
    )
)

# Export the Web App endpoint
pulumi.export('endpoint', app.default_host_name.apply(
    lambda default_host_name: f"https://{default_host_name}"
))

# Export Resource Group details
pulumi.export("resource_group_name", resource_group.name)
pulumi.export("resource_group_location", resource_group.location)

# Export Storage Account details
pulumi.export("storage_account_name", storage_account.name)
pulumi.export("storage_account_sku", storage_account.sku.name)
pulumi.export("storage_account_kind", storage_account.kind)

# Export Blob Container details
pulumi.export("blob_container_name", zip_container.name)

# Export Blob URL
pulumi.export("blob_url", blob_url)

# Export Application Insights details
pulumi.export("app_insights_name", app_insights.name)
pulumi.export("app_insights_kind", app_insights.kind)
pulumi.export("app_insights_application_type", app_insights.application_type)

# Export App Service Plan details
pulumi.export("app_service_plan_name", app_service_plan.name)
pulumi.export("app_service_plan_sku_tier", app_service_plan.sku.tier)
pulumi.export("app_service_plan_kind", app_service_plan.kind)

# Export Web App details
pulumi.export('web_app_name', app.name)
pulumi.export('web_app_location', resource_group.location)
pulumi.export('web_app_linux_fx_version', 'PYTHON|3.9')

