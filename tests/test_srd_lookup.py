import pytest

from app.srd.lookup import lookup


def test_lookup_success() -> None:
    goblin = lookup("SRD.goblin")
    assert goblin["name"] == "Goblin"


def test_lookup_fail() -> None:
    with pytest.raises(KeyError):
        lookup("SRD.unknown")
