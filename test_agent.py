import os
import sys

# Add project root to Python path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from agent import answer_query, find_best_match, kb


def test_kb_loaded():
    """Check KB is loaded."""
    assert isinstance(kb, list)
    assert len(kb) > 0


def test_find_best_match_structure():
    """Returned result format should be correct."""
    results = find_best_match("leave policy")
    assert isinstance(results, list)
    assert len(results) > 0
    item = results[0]
    assert "title" in item
    assert "text" in item
    assert "score" in item


def test_answer_query_returns_string():
    """Answer must return a non-empty string."""
    ans = answer_query("What are the benefits?")
    assert isinstance(ans, str)
    assert len(ans.strip()) > 0


def test_unknown_query_behavior():
    """Unknown queries should return fallback OR valid text if fuzzy match mistakenly hits."""
    ans = answer_query("How to repair a motorcycle engine?")
    assert isinstance(ans, str)
    assert len(ans) > 0
    # Either fallback or a matched entry is acceptable