"""
Unit tests for humanize.lists module.
Module Author  : 24P-3060
Functions Under Test:
    - humanize.natural_list()

Test Design Techniques Applied:
    - Equivalence Class Partitioning (ECP): empty, single-item, two-item, multi-item lists
    - Boundary Value Analysis (BVA): 0, 1, 2, 3, and large list sizes
    - Parameterization: data-driven tables for various list inputs
"""

import pytest
import humanize


# ─────────────────────────────────────────────────────────────────────────────
# natural_list – converts a Python list to a natural language string
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.lists
@pytest.mark.smoke
@pytest.mark.order(1)
class TestNaturalListBasic:
    """
    Basic tests for humanize.natural_list().
    ECP partitions: empty, single, two-element, multi-element lists.
    """

    def test_emptyList(self):
        """BVA: empty list → empty string."""
        assert humanize.natural_list([]) == ""

    def test_singleItem(self):
        """BVA: single item → returns that item with no 'and'."""
        assert humanize.natural_list(["apple"]) == "apple"

    def test_twoItemsUsesAnd(self):
        """BVA: two items → joined with 'and' (no comma)."""
        result = humanize.natural_list(["apple", "banana"])
        assert result == "apple and banana"

    def test_threeItemsNoOxfordComma(self):
        """ECP: three items → comma-separated, 'and' at end WITHOUT Oxford comma."""
        result = humanize.natural_list(["apple", "banana", "cherry"])
        assert result == "apple, banana and cherry"

    def test_fourItems(self):
        """ECP: four items → comma-separated with 'and' at end."""
        result = humanize.natural_list(["a", "b", "c", "d"])
        assert result == "a, b, c and d"

    def test_returnsString(self):
        """natural_list always returns a string."""
        assert isinstance(humanize.natural_list(["x", "y"]), str)

    @pytest.mark.parametrize("lst, expected", [
        ([],                      ""),
        (["one"],                 "one"),
        (["one", "two"],          "one and two"),
        (["one", "two", "three"], "one, two and three"),
    ])
    def test_parametrizedBasicLists(self, lst, expected):
        """ECP parametrized: various list sizes produce expected output."""
        assert humanize.natural_list(lst) == expected


@pytest.mark.lists
@pytest.mark.order(2)
class TestNaturalListOutputStructure:
    """Tests verifying the structural properties of natural_list output."""

    def test_twoItemNoComma(self):
        """ECP: exactly 2 items produces NO comma – just 'X and Y'."""
        result = humanize.natural_list(["red", "blue"])
        assert "," not in result
        assert "and" in result

    def test_threeItemsHasComma(self):
        """ECP: 3 items uses commas before the final 'and'."""
        result = humanize.natural_list(["x", "y", "z"])
        assert "," in result
        assert "and" in result

    def test_andAppearsExactlyOnce(self):
        """ECP: 'and' appears exactly once regardless of list size."""
        result = humanize.natural_list(["a", "b", "c", "d", "e"])
        assert result.count(" and ") == 1

    def test_outputContainsAllItems(self):
        """ECP: all items appear in the output string."""
        items = ["cat", "dog", "fish"]
        result = humanize.natural_list(items)
        for item in items:
            assert item in result

    def test_fiveItemsStructure(self):
        """ECP: 5 items – verify comma count and structure."""
        result = humanize.natural_list(["a", "b", "c", "d", "e"])
        # Should be "a, b, c, d and e" — 3 commas
        assert result == "a, b, c, d and e"


@pytest.mark.lists
@pytest.mark.order(3)
class TestNaturalListEdgeCases:
    """Edge case tests for natural_list()."""

    def test_listWithNumbers(self):
        """ECP: list containing integers is converted to strings."""
        result = humanize.natural_list([1, 2, 3])
        assert "1" in result and "2" in result and "3" in result

    def test_listWithEmptyStringItem(self):
        """ECP: list containing an empty string item."""
        result = humanize.natural_list(["", "b"])
        assert "and" in result
        assert isinstance(result, str)

    def test_largeList(self):
        """BVA: large list (10 items) → all joined correctly."""
        items = [str(i) for i in range(10)]
        result = humanize.natural_list(items)
        assert "and" in result
        assert isinstance(result, str)
        for item in items:
            assert item in result

    def test_singleNumberItem(self):
        """BVA: single numeric item."""
        result = humanize.natural_list([42])
        assert "42" in result

    def test_listWithSpecialCharacters(self):
        """ECP: items containing special characters."""
        result = humanize.natural_list(["hello!", "world?"])
        assert "hello!" in result
        assert "world?" in result

    def test_singleItemNoAnd(self):
        """BVA: single item should contain NO 'and'."""
        result = humanize.natural_list(["solo"])
        assert "and" not in result
        assert result == "solo"
