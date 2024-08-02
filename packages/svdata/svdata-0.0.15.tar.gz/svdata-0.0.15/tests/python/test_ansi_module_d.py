from svdata import SvNetType, SvPortDirection, read_sv_file

ansi_module_d = read_sv_file("tests/systemverilog/ansi_module_d.sv").modules[0]


def test_module():
    assert ansi_module_d.ports[0].identifier == "a"
    assert ansi_module_d.ports[0].direction == SvPortDirection.Input
    assert ansi_module_d.ports[0].net_type is None

    assert ansi_module_d.ports[1].identifier == "b"
    assert ansi_module_d.ports[1].direction == SvPortDirection.Input
    assert ansi_module_d.ports[1].net_type is None

    assert ansi_module_d.ports[2].identifier == "c"
    assert ansi_module_d.ports[2].direction == SvPortDirection.Output
    assert ansi_module_d.ports[2].net_type == SvNetType.Tri

    assert ansi_module_d.ports[3].identifier == "d"
    assert ansi_module_d.ports[3].direction == SvPortDirection.Input
    assert ansi_module_d.ports[3].net_type == SvNetType.Wire

    assert ansi_module_d.ports[4].identifier == "e"
    assert ansi_module_d.ports[4].direction == SvPortDirection.Inout
    assert ansi_module_d.ports[4].net_type == SvNetType.Wire
