"""Unit tests for interaction filtering logic — edge cases and boundary values."""

from app.models.interaction import InteractionLog
from app.routers.interactions import filter_by_max_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    """Helper to create an InteractionLog for testing."""
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")

# KEPT: Tests that max_item_id=0 excludes all positive item_ids
def test_filter_max_item_id_zero_excludes_positive() -> None:
    """max_item_id=0 should exclude all interactions with positive item_id."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2), _make_log(3, 3, 3)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=0)
    assert result == []

# KEPT: Tests negative max_item_id excludes all positive items
def test_filter_negative_max_item_id_excludes_all_positive() -> None:
    """Negative max_item_id should exclude all interactions with positive item_id."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 5), _make_log(3, 3, 10)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=-1)
    assert result == []

# KEPT: Tests max_item_id equal to maximum item_id includes all
def test_filter_max_item_id_equals_max_in_list() -> None:
    """max_item_id equal to the maximum item_id should include that element."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 5), _make_log(3, 3, 10)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=10)
    assert len(result) == 3
    assert all(i.item_id <= 10 for i in result)

# KEPT: Tests when all item_ids are greater than max
def test_filter_all_item_ids_greater_than_max() -> None:
    """When all item_ids are greater than max_item_id, result should be empty."""
    interactions = [_make_log(1, 1, 10), _make_log(2, 2, 20), _make_log(3, 3, 30)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
    assert result == []

# KEPT: Tests when all item_ids equal max
def test_filter_all_item_ids_equal_to_max() -> None:
    """When all item_ids equal max_item_id, all should be included."""
    interactions = [_make_log(1, 1, 5), _make_log(2, 2, 5), _make_log(3, 3, 5)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
    assert len(result) == 3
    assert all(i.item_id == 5 for i in result)

# KEPT: Tests with duplicate item_ids
def test_filter_with_duplicate_item_ids() -> None:
    """Duplicate item_ids should all be preserved if they pass the filter."""
    interactions = [
        _make_log(1, 1, 3),
        _make_log(2, 2, 3),
        _make_log(3, 3, 3),
        _make_log(4, 4, 5),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=3)
    assert len(result) == 3
    assert all(i.item_id == 3 for i in result)

# KEPT: Tests very large max_item_id returns all
def test_filter_very_large_max_item_id_returns_all() -> None:
    """A very large max_item_id should return all interactions."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 100), _make_log(3, 3, 1000)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=999999)
    assert len(result) == 3

# KEPT: Tests single element passes
def test_filter_single_element_passes() -> None:
    """Single element with item_id <= max_item_id should be returned."""
    interactions = [_make_log(1, 1, 5)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=10)
    assert len(result) == 1
    assert result[0].id == 1

# KEPT: Tests single element filtered out
def test_filter_single_element_filtered_out() -> None:
    """Single element with item_id > max_item_id should be filtered out."""
    interactions = [_make_log(1, 1, 10)]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=5)
    assert result == []

# KEPT: Tests item_id=0 in data
def test_filter_with_item_id_zero_in_data() -> None:
    """Interactions with item_id=0 should be included when max_item_id >= 0."""
    interactions = [
        _make_log(1, 1, 0),
        _make_log(2, 2, 1),
        _make_log(3, 3, 2),
    ]
    result = filter_by_max_item_id(interactions=interactions, max_item_id=1)
    assert len(result) == 2
    assert all(i.item_id <= 1 for i in result)
    assert any(i.item_id == 0 for i in result)
# DISCARDED: This test duplicates boundary coverage from original test file
# def test_filter_boundary_duplicate() -> None:
#     """Duplicate test - already covered in test_interactions.py"""
#     pass