import pytest
from baserowapi.models.row import Row
from baserowapi.models.field import TextField
import logging


# Fixture for the mock Baserow client
@pytest.fixture
def mock_client():
    class MockClient:
        def make_api_request(self, endpoint, method="GET", data=None):
            return {}

    return MockClient()


# Mock field class that subclasses TextField
class MockTextField(TextField):
    def __init__(self, name):
        super().__init__(name=name, field_data={"type": "text"})


# Fixture for the mock Table object
@pytest.fixture
def mock_table(mock_client):
    class MockTable:
        def __init__(self):
            self.id = "sample_table_id"
            self.table_id = "sample_table_id"
            self.fields = {
                "field1": MockTextField("field1"),
                "field2": MockTextField("field2"),
            }

    return MockTable()


def test_row_initialization_with_given_data(mock_table, mock_client):
    # Sample row data for testing
    row_data = {
        "id": "sample_id",
        "order": "sample_order",
        "field1": "value1",
        "field2": "value2",
    }

    # Initialize the Row object
    row = Row(row_data=row_data, table=mock_table, client=mock_client)

    # Assertions
    assert row.id == row_data["id"]
    assert row.order == row_data["order"]
    assert row._row_data == row_data
    assert row.table_id == mock_table.table_id


def test_row_table_id_is_correctly_set_from_table_object(mock_table, mock_client):
    # Sample row data for testing
    row_data = {
        "id": "sample_id",
        "order": "sample_order",
        "field1": "value1",
        "field2": "value2",
    }

    # Initialize the Row object
    row = Row(row_data=row_data, table=mock_table, client=mock_client)

    # Assertion
    assert (
        row.table_id == mock_table.table_id
    ), f"Expected table_id to be {mock_table.table_id}, but got {row.table_id}."


def test_row_repr_method(mock_table, mock_client):
    # Sample row data for testing
    row_data = {
        "id": "sample_id",
        "order": "sample_order",
        "field1": "value1",
        "field2": "value2",
    }

    # Initialize the Row object
    row = Row(row_data=row_data, table=mock_table, client=mock_client)

    # Expected representation
    expected_repr = f"Row id {row_data['id']} of table {mock_table.table_id}"

    # Assertion
    assert (
        str(row) == expected_repr
    ), f"Expected repr to be {expected_repr}, but got {str(row)}."


@pytest.fixture
def sample_row_data():
    return {"id": "sample_id", "order": "sample_order", "field1": "value1"}


@pytest.fixture
def sample_row(mock_table, mock_client, sample_row_data):
    return Row(table=mock_table, client=mock_client, row_data=sample_row_data)


def test_getitem_method(sample_row):
    assert sample_row["field1"] == "value1"


def test_getitem_method_non_existent_field(caplog, sample_row):
    with caplog.at_level(logging.WARNING):
        with pytest.raises(KeyError):
            sample_row["non_existent_field"]
    assert "Field 'non_existent_field' not found in row values." in caplog.text


def test_setitem_method(sample_row):
    sample_row["field1"] = "new_value"
    assert sample_row["field1"] == "new_value"


def test_setitem_method_new_field(caplog, sample_row):
    with caplog.at_level(logging.WARNING):
        with pytest.raises(KeyError):
            sample_row["new_field"] = "new_value"
    assert (
        "Attempted to set a value for an unrecognized field 'new_field' in the row."
        in caplog.text
    )


def test_update_fields_correctly_updates_fields(sample_row):
    update_data = {"field1": "updated_value"}
    sample_row.update(update_data)
    assert sample_row["field1"] == "updated_value"


def test_update_fields_raises_keyerror_for_non_existent_fields(sample_row):
    update_data = {"non_existent_field": "some_value"}
    with pytest.raises(
        KeyError,  # Changed from ValueError to KeyError
        match="Field 'non_existent_field' not found in row.",  # Adjust the match string if necessary
    ):
        sample_row.update(update_data)


# Extend the mock_client to include a method to mock the API request
@pytest.fixture
def mock_client_with_update_request(mocker):
    class _mock_client:
        def __init__(self):
            self.should_fail = False

        def make_api_request(self, *args, **kwargs):
            if self.should_fail:
                raise Exception("API request failed.")
            else:
                return {
                    "id": "sample_id",
                    "order": "sample_order",
                    "field1": "updated_value",
                }

    return _mock_client()


# Extend the mock_client to include a method to mock the DELETE API request
@pytest.fixture
def mock_client_with_delete_request(mocker):
    class _mock_client:
        def __init__(self):
            self.should_fail = False

        def make_api_request(self, endpoint, method="GET", data=None):
            if method == "DELETE":
                if self.should_fail:
                    raise Exception("API delete request failed.")
                else:
                    return 204  # Simulating a 204 No Content response for successful delete
            else:
                return {
                    "id": "sample_id",
                    "order": "sample_order",
                    "field1": "updated_value",
                }

    return _mock_client()


def test_delete_method_successfully_sends_delete_request(
    mock_client_with_delete_request, sample_row
):
    sample_row.client = mock_client_with_delete_request
    result = sample_row.delete()
    assert result is True


def test_delete_method_logs_error_and_raises_exception_on_failed_api_request(
    mock_client_with_delete_request, sample_row, caplog
):
    # Setting up the client to fail
    mock_client_with_delete_request.should_fail = True
    sample_row.client = mock_client_with_delete_request

    # Checking if an error is logged and an exception is raised
    with caplog.at_level(logging.ERROR):
        with pytest.raises(Exception, match="API delete request failed."):
            sample_row.delete()

    assert (
        "Failed to delete row with ID sample_id from table sample_table_id. Error: API delete request failed."
        in caplog.text
    )
