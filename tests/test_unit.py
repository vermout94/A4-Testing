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


### Unit Tests

def test_resource_group(pulumi_stack):
    """
    Tests the Resource Group configuration.
    """
    resource_group_name = pulumi_stack.get("resource_group_name")
    assert resource_group_name is not None, "Resource group name is missing"
    assert resource_group_name.startswith("resourceGroup"), "Resource group name has an unexpected prefix"

    resource_group_location = pulumi_stack.get("resource_group_location")
    assert resource_group_location == "westeurope", "Resource group location is incorrect"


def test_storage_account(pulumi_stack):
    """
    Tests the Storage Account configuration.
    """
    storage_account_name = pulumi_stack.get("storage_account_name")
    assert storage_account_name.startswith("storageaccount"), "Storage account name prefix is incorrect"

    storage_account_sku = pulumi_stack.get("storage_account_sku")
    assert storage_account_sku == "Standard_LRS", "Storage account SKU is incorrect"

    storage_account_kind = pulumi_stack.get("storage_account_kind")
    assert storage_account_kind == "StorageV2", "Storage account kind is incorrect"


def test_blob_container(pulumi_stack):
    """
    Tests the Blob Container configuration.
    """
    blob_container_name = pulumi_stack.get("blob_container_name")
    assert blob_container_name == "zipcontainer", "Blob container name is incorrect"
