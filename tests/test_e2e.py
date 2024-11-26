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

### End-to-End Tests

def test_web_app(pulumi_stack):
    """
    Tests the Web App deployment.
    """
    web_app_name = pulumi_stack.get("web_app_name")
    assert web_app_name.startswith("webApp"), "Web App name prefix is incorrect"

    web_app_location = pulumi_stack.get("web_app_location")
    assert web_app_location == "westeurope", "Web App location is incorrect"

    web_app_linux_fx_version = pulumi_stack.get("web_app_linux_fx_version")
    assert web_app_linux_fx_version == "PYTHON|3.9", "Web App runtime version is incorrect"


def test_end_to_end_stack(pulumi_stack):
    """
    Verifies that all major resources are correctly created and related.
    """
    assert pulumi_stack.get("resource_group_name") is not None, "Resource group is not created"
    assert pulumi_stack.get("storage_account_name") is not None, "Storage account is not created"
    assert pulumi_stack.get("blob_container_name") is not None, "Blob container is not created"
    assert pulumi_stack.get("app_service_plan_name") is not None, "App Service Plan is not created"
    assert pulumi_stack.get("web_app_name") is not None, "Web App is not created"
    assert pulumi_stack.get("app_insights_name") is not None, "Application Insights is not created"