import pytest
from pulumi import automation as auto


@pytest.fixture(scope="module")
def pulumi_stack():
    """
    Loads an existing Pulumi stack for testing.
    """
    project_name = "A4-Testing"
    stack_name = "dev"

    # Pulumi Automation API: Load the stack
    stack = auto.select_stack(
        stack_name=stack_name,
        project_name=project_name,
        program=lambda: None,
    )

    try:
        outputs = stack.outputs()
        resolved_outputs = {key: value.value for key, value in outputs.items()}
        return resolved_outputs
    except Exception as e:
        print(f"Error loading stack outputs: {e}")
        raise e

### Integration Tests

def test_blob_url(pulumi_stack):
    """
    Tests the Blob URL.
    """
    blob_url = pulumi_stack.get("blob_url")
    assert blob_url.startswith("https://"), "Blob URL does not start with HTTPS"
    assert "blob.core.windows.net/zipcontainer/hello-world.zip" in blob_url, "Blob URL is incorrect or malformed"


def test_app_service_plan(pulumi_stack):
    """
    Tests the App Service Plan configuration.
    """
    app_service_plan_name = pulumi_stack.get("app_service_plan_name")
    assert app_service_plan_name.startswith("appServicePlan"), "App Service Plan name prefix is incorrect"

    app_service_plan_sku_tier = pulumi_stack.get("app_service_plan_sku_tier")
    assert app_service_plan_sku_tier == "Free", "App Service Plan SKU tier is incorrect"

    app_service_plan_kind = pulumi_stack.get("app_service_plan_kind")
    assert app_service_plan_kind == "linux", "App Service Plan kind is incorrect"


def test_application_insights(pulumi_stack):
    """
    Tests the Application Insights configuration.
    """
    app_insights_name = pulumi_stack.get("app_insights_name")
    assert app_insights_name.startswith("appInsights"), "Application Insights name prefix is incorrect"

    app_insights_application_type = pulumi_stack.get("app_insights_application_type")
    assert app_insights_application_type == "web", "Application Insights application type is incorrect"

    app_insights_kind = pulumi_stack.get("app_insights_kind")
    assert app_insights_kind == "web", "Application Insights kind is incorrect"