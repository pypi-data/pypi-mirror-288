from hypothesis import given

from osrparse.strategies import replays

from circleguard.investigations import Investigations
from circleguard import KeylessCircleguard
from circleguard.loadables import ReplayOsrparse

cg = KeylessCircleguard()

@given(replays(), replays())
def test_similarity(r1, r2):
    r1 = ReplayOsrparse(r1)
    r2 = ReplayOsrparse(r2)
    cg.load(r1)
    cg.load(r2)
    sim = Investigations.similarity(
        r1,
        r2,
        method="similarity",
        num_chunks=20,
        mods_unknown="best"
    )
    assert sim >= 0
