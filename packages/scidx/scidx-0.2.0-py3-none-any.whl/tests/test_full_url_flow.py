import pytest
import uuid
from scidx.client import sciDXClient

# Function to generate a unique organization name
def generate_unique_name(base_name):
    return f"{base_name}_{uuid.uuid4().hex[:6]}"

# Global variables to store IDs and names
api_url = "http://127.0.0.1:8000"
USERNAME = "placeholder@placeholder.com"
PASSWORD = "placeholder"
client = sciDXClient(api_url)
organization_name = generate_unique_name("pytest_organization")
organization_data = {
    "name": organization_name,
    "title": "Pytest Organization",
    "description": "Organization created for pytest."
}
url_data = {
    "resource_name": generate_unique_name("pytest_resource"),
    "resource_title": "Pytest Resource Title",
    "owner_org": organization_name,
    "resource_url": "http://example.com/resource",
    "notes": "This is a resource for testing.",
    "extras": {"key1": "value1", "key2": "value2"}
}

@pytest.fixture(scope="module", autouse=True)
def setup_and_cleanup():
    global client, organization_name, organization_data, url_data

    # Login to the client
    client.login(USERNAME, PASSWORD)

    # Setup: Ensure the organization does not already exist
    print("Setup: Checking if the organization already exists")
    existing_orgs = client.search_organization()
    print(f"Setup: Existing organizations: {existing_orgs}")
    if organization_name in existing_orgs:
        print(f"Setup: Organization {organization_name} already exists")
        client.delete_organization(organization_name)
        print(f"Setup: Deleted existing organization {organization_name}")

    # Run the tests
    yield

    # Cleanup: Delete the organization after tests
    try:
        client.delete_organization(organization_name)
        print(f"Cleanup: Deleted organization {organization_name}")
    except Exception as e:
        print(f"Cleanup: Failed to delete organization {organization_name}. Reason: {str(e)}")

# Test to create an organization
@pytest.mark.order(1)
def test_create_organization():
    global client, organization_data
    response = client.register_organization(**organization_data)
    assert "id" in response
    assert response["message"] == "Organization created successfully"

# Test to register a URL resource
@pytest.mark.order(2)
def test_register_url():
    global client, url_data
    response = client.register_url(**url_data)
    assert "id" in response
    assert response["id"] is not None

# Test to search for URL resource by name
@pytest.mark.order(3)
def test_search_resource_by_name():
    global client, url_data
    response = client.search_resource(resource_name=url_data["resource_name"])
    assert len(response) > 0
    assert response[0]["name"] == url_data["resource_name"]

# Test to search for URL resource by organization ID
@pytest.mark.order(4)
def test_search_resource_by_organization():
    global client, url_data
    response = client.search_resource(owner_org=url_data["owner_org"])
    assert len(response) > 0
    assert response[0]["owner_org"] == url_data["owner_org"]

# Test to search for URL resource by search term
@pytest.mark.order(5)
def test_search_resource_by_term():
    global client
    search_term = "Pytest"
    response = client.search_resource(search_term=search_term)
    assert len(response) > 0
    assert any(search_term in result["title"] for result in response)

# Test to search for URL resource by owner_org and other parameters
@pytest.mark.order(6)
def test_search_resource_by_owner_org_and_other_params():
    global client, url_data
    search_term = "Pytest"
    resource_name = url_data["resource_name"]
    response = client.search_resource(
        owner_org=url_data["owner_org"],
        resource_name=resource_name,
        search_term=search_term
    )
    assert len(response) > 0
    assert all(result["owner_org"] == url_data["owner_org"] for result in response)
    assert any(search_term in result["title"] or result["name"] == resource_name for result in response)
import pytest
import uuid
from scidx.client import sciDXClient

# Function to generate a unique organization name
def generate_unique_name(base_name):
    return f"{base_name}_{uuid.uuid4().hex[:6]}"

# Global variables to store IDs and names
api_url = "http://127.0.0.1:8000"
USERNAME = "placeholder@placeholder.com"
PASSWORD = "placeholder"
client = sciDXClient(api_url)
organization_name = generate_unique_name("pytest_organization")
organization_data = {
    "name": organization_name,
    "title": "Pytest Organization",
    "description": "Organization created for pytest."
}
url_data = {
    "resource_name": generate_unique_name("pytest_resource"),
    "resource_title": "Pytest Resource Title",
    "owner_org": organization_name,
    "resource_url": "http://example.com/resource",
    "notes": "This is a resource for testing.",
    "extras": {"key1": "value1", "key2": "value2"}
}

@pytest.fixture(scope="module", autouse=True)
def setup_and_cleanup():
    global client, organization_name, organization_data, url_data

    # Login to the client
    client.login(USERNAME, PASSWORD)

    # Setup: Ensure the organization does not already exist
    print("Setup: Checking if the organization already exists")
    existing_orgs = client.search_organization()
    print(f"Setup: Existing organizations: {existing_orgs}")
    if organization_name in existing_orgs:
        print(f"Setup: Organization {organization_name} already exists")
        client.delete_organization(organization_name)
        print(f"Setup: Deleted existing organization {organization_name}")

    # Run the tests
    yield

    # Cleanup: Delete the organization after tests
    try:
        client.delete_organization(organization_name)
        print(f"Cleanup: Deleted organization {organization_name}")
    except Exception as e:
        print(f"Cleanup: Failed to delete organization {organization_name}. Reason: {str(e)}")

# Test to create an organization
@pytest.mark.order(1)
def test_create_organization():
    global client, organization_data
    response = client.register_organization(**organization_data)
    assert "id" in response
    assert response["message"] == "Organization created successfully"

# Test to register a URL resource
@pytest.mark.order(2)
def test_register_url():
    global client, url_data
    response = client.register_url(**url_data)
    assert "id" in response
    assert response["id"] is not None

# Test to search for URL resource by name
@pytest.mark.order(3)
def test_search_resource_by_name():
    global client, url_data
    response = client.search_resource(resource_name=url_data["resource_name"])
    assert len(response) > 0
    assert response[0]["name"] == url_data["resource_name"]

# Test to search for URL resource by organization ID
@pytest.mark.order(4)
def test_search_resource_by_organization():
    global client, url_data
    response = client.search_resource(owner_org=url_data["owner_org"])
    assert len(response) > 0
    assert response[0]["owner_org"] == url_data["owner_org"]

# Test to search for URL resource by search term
@pytest.mark.order(5)
def test_search_resource_by_term():
    global client
    search_term = "Pytest"
    response = client.search_resource(search_term=search_term)
    assert len(response) > 0
    assert any(search_term in result["title"] for result in response)

# Test to search for URL resource by owner_org and other parameters
@pytest.mark.order(6)
def test_search_resource_by_owner_org_and_other_params():
    global client, url_data
    search_term = "Pytest"
    resource_name = url_data["resource_name"]
    response = client.search_resource(
        owner_org=url_data["owner_org"],
        resource_name=resource_name,
        search_term=search_term
    )
    assert len(response) > 0
    assert all(result["owner_org"] == url_data["owner_org"] for result in response)
    assert any(search_term in result["title"] or result["name"] == resource_name for result in response)
