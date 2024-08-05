from supply import collect
from dataclasses import dataclass
from circleguard import Mod
from ossapi import Ossapi, Domain

@dataclass
class A:
    a: int
class B:
    c: str

with collect():
    def myfunctionlongname(v):
        return v
    myfunctionlongname("a")

    m = Mod("HD")
    for i in range(100):
        a = A(i)
    o = Ossapi(3763, "KEY", domain="osu")
    o_lazer = Ossapi(3763, "KEY", domain="lazer")

    o.user("tybug")
    o_lazer.user("tybug")



def test_a():
    from supply.pool import A, Mod, Ossapi

    a = A(a=5)
    assert a.a == 5

    a = A(a=lambda a: a != 2)
    assert a.a != 2

    m = Mod("HD")
    assert m.value == 8
    m = Mod(_value_=8)
    assert m.value == 8


    o = Ossapi(domain="osu")
    assert o.domain == Domain.OSU
    u = o.user("tybug")
    assert u.username == "tybug"

    o = Ossapi(_domain_=Domain.OSU)
    assert o.domain == Domain.OSU



    # ---
    api = Ossapi(_domain_=Domain.OSU)
    api_lazer = Ossapi(_domain_=Domain.LAZER)
    u = api.user("tybug")
    u_lazer = api_lazer.user("tybug")

    pp = u.statistics.pp
    pp_exp = u.statistics.pp_exp
    pp_lazer = u_lazer.statistics.pp
    pp_exp_lazer = u_lazer.statistics.pp_exp

    assert pp_exp_lazer == 0
    assert pp != pp_lazer
    assert pp_exp == pp_lazer
    # ---




test_a()
