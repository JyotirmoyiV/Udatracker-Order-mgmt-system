import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

#
# --- TODO: add test functions below this line ---
#
def test_add_order_success(order_tracker, mock_storage):
    result = order_tracker.add_order(
        "ORD001",
        "Laptop",
        1,
        "CUST001"
    )

    expected = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }

    assert result == expected
    mock_storage.save_order.assert_called_once_with("ORD001", expected)

def test_add_duplicate_order_raises_error(order_tracker, mock_storage):
    mock_storage.get_order.return_value = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }

    with pytest.raises(
        ValueError,
        match="Order with ID 'ORD001' already exists."
    ):
        order_tracker.add_order(
            "ORD001",
            "Laptop",
            1,
            "CUST001"
        )
    
def test_get_order_by_id_success(order_tracker, mock_storage):
    expected = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }

    mock_storage.get_order.return_value = expected

    result = order_tracker.get_order_by_id("ORD001")

    assert result == expected
    mock_storage.get_order.assert_called_once_with("ORD001")

def test_get_order_by_id_not_found(order_tracker, mock_storage):
    mock_storage.get_order.return_value = None

    result = order_tracker.get_order_by_id("NONEXISTENT")

    assert result is None
    mock_storage.get_order.assert_called_once_with("NONEXISTENT")


def test_get_order_by_id_empty_id_raises_error(order_tracker):
    with pytest.raises(
        ValueError,
        match="Order ID cannot be empty."
    ):
        order_tracker.get_order_by_id("")  

def test_update_order_status_success(order_tracker, mock_storage):
    existing_order = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending"
    }

    mock_storage.get_order.return_value = existing_order

    result = order_tracker.update_order_status(
        "ORD001",
        "shipped"
    )

    assert result["status"] == "shipped"

    expected = existing_order.copy()
    expected["status"] = "shipped"

    mock_storage.save_order.assert_called_once_with(
        "ORD001",
        expected
    )

def test_update_order_status_invalid_status(order_tracker, mock_storage):
    with pytest.raises(ValueError):
        order_tracker.update_order_status(
            "ORD001",
            "invalid"
        )

    # Invalid status should fail before storage is read
    mock_storage.get_order.assert_not_called()


def test_update_order_status_order_not_found(order_tracker, mock_storage):
    mock_storage.get_order.return_value = None

    with pytest.raises(ValueError):
        order_tracker.update_order_status(
            "ORD404",
            "shipped"
        )


def test_update_order_status_empty_id(order_tracker):
    with pytest.raises(
        ValueError,
        match="Order ID cannot be empty."
    ):
        order_tracker.update_order_status(
            "",
            "shipped"
        )

def test_list_all_orders_returns_empty_list(order_tracker, mock_storage):
    mock_storage.get_all_orders.return_value = {}

    result = order_tracker.list_all_orders()

    assert result == []


def test_list_all_orders_returns_all_orders(order_tracker, mock_storage):
    orders = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending"
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Mouse",
            "quantity": 2,
            "customer_id": "CUST002",
            "status": "shipped"
        }
    }

    mock_storage.get_all_orders.return_value = orders

    result = order_tracker.list_all_orders()

    assert len(result) == 2
    assert orders["ORD001"] in result
    assert orders["ORD002"] in result

    def test_list_orders_by_status_returns_matching_orders(order_tracker, mock_storage):
        orders = {
            "ORD001": {
                "order_id": "ORD001",
                "status": "pending"
            },
            "ORD002": {
                "order_id": "ORD002",
                "status": "shipped"
            },
            "ORD003": {
                "order_id": "ORD003",
                "status": "pending"
            }
        }

        mock_storage.get_all_orders.return_value = orders

        result = order_tracker.list_orders_by_status("pending")

        assert {order["order_id"] for order in result} == {
            "ORD001",
            "ORD003"
    }


def test_list_orders_by_status_returns_empty_list(order_tracker, mock_storage):
    mock_storage.get_all_orders.return_value = {}

    result = order_tracker.list_orders_by_status("pending")

    assert result == []


def test_list_orders_by_status_invalid_status(order_tracker):
    with pytest.raises(ValueError):
        order_tracker.list_orders_by_status("invalid")


def test_list_orders_by_status_empty_status(order_tracker):
    with pytest.raises(ValueError):
        order_tracker.list_orders_by_status("")