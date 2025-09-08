# This file is part of sphinx-roles.
#
# Copyright 2025 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License version 3, as published by the Free
# Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranties of MERCHANTABILITY, SATISFACTORY
# QUALITY, or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

import pytest
from docutils import nodes
from sphinx import addnodes
from sphinx_roles.roles import LiteralrefRole, NoneRole, SpellExceptionRole
from typing_extensions import override


class FakeSpellExceptionRole(SpellExceptionRole):
    @override
    def __init__(self, text):
        self.text = text


class FakeNoneRole(NoneRole):
    @override
    def __init__(self, text):
        self.text = text


class FakeLiteralrefRole(LiteralrefRole):
    @override
    def __init__(self, title, target):
        self.title = title
        self.target = target


@pytest.fixture
def fake_spellexception_role(request: pytest.FixtureRequest) -> FakeSpellExceptionRole:
    """This fixture can be parametrized to override the default values."""
    # Get any optional overrides from the fixtures
    overrides = request.param if hasattr(request, "param") else {}

    return FakeSpellExceptionRole(text=overrides.get("text", ""))


@pytest.fixture
def fake_none_role(request: pytest.FixtureRequest) -> FakeNoneRole:
    """This fixture can be parametrized to override the default values."""
    # Get any optional overrides from the fixtures
    overrides = request.param if hasattr(request, "param") else {}

    return FakeNoneRole(text=overrides.get("text", ""))


@pytest.fixture
def fake_literalref_role(request: pytest.FixtureRequest) -> FakeLiteralrefRole:
    """This fixture can be parametrized to override the default values."""
    # Get any optional overrides from the fixtures
    overrides = request.param if hasattr(request, "param") else {}

    return FakeLiteralrefRole(
        title=overrides.get("title", ""), target=overrides.get("target", "")
    )


@pytest.mark.parametrize(
    "fake_none_role",
    [{"text": "this does nothing."}],
    indirect=True,
)
def test_none_role(fake_none_role: FakeNoneRole):
    expected: tuple[list[nodes.Node], list[nodes.system_message]] = [], []
    actual = fake_none_role.run()

    assert str(expected) == str(actual)


@pytest.mark.parametrize(
    "fake_spellexception_role",
    [{"text": "wow."}],
    indirect=True,
)
def test_spellexception_role(fake_spellexception_role: FakeSpellExceptionRole):
    node = nodes.raw(text="<spellexception>wow.</spellexception>", format="html")
    expected: tuple[list[nodes.Node], list[nodes.system_message]] = [node], []

    actual = fake_spellexception_role.run()

    assert str(expected) == str(actual)


@pytest.mark.parametrize(
    "fake_literalref_role",
    [{"title": "link text", "target": "label"}],
    indirect=True,
)
def test_literalref_internal(fake_literalref_role: FakeLiteralrefRole):
    return_nodes: list[nodes.Node] = []
    ref_node = addnodes.pending_xref(
        "",
        refdomain="lrd",
        reftype="ref",
        reftarget="label",
        refexplicit=True,
        refwarning=True,
    )
    ref_node.append(nodes.literal(text="link text"))
    return_nodes.append(ref_node)
    expected: tuple[list[nodes.Node], list[nodes.system_message]] = return_nodes, []

    actual = fake_literalref_role.run()

    assert str(expected) == str(actual)


@pytest.mark.parametrize(
    "fake_literalref_role",
    [
        {
            "title": "link text",
            "target": "https://github.com/canonical/sphinx-roles",
        }
    ],
    indirect=True,
)
def test_literalref_external(fake_literalref_role: FakeLiteralrefRole):
    return_nodes: list[nodes.Node] = []
    ref_node = nodes.reference(
        "",
        "",
        internal=False,
        refuri="https://github.com/canonical/sphinx-roles",
    )
    ref_node.append(nodes.literal(text="link text"))
    return_nodes.append(ref_node)
    expected: tuple[list[nodes.Node], list[nodes.system_message]] = return_nodes, []

    actual = fake_literalref_role.run()

    assert str(expected) == str(actual)


@pytest.mark.parametrize(
    "fake_literalref_role",
    [
        {
            "title": "link text",
            "target": "https://github.com/canonical/sphinx-roles",
        }
    ],
    indirect=True,
)
def test_literalref_external_no_prefix(fake_literalref_role: FakeLiteralrefRole):
    return_nodes: list[nodes.Node] = []
    ref_node = nodes.reference(
        "",
        "",
        internal=False,
        refuri="github.com/jahn-junior/sphinx-roles",
    )
    ref_node.append(nodes.literal(text="link text"))
    return_nodes.append(ref_node)
    expected: tuple[list[nodes.Node], list[nodes.system_message]] = return_nodes, []

    actual = fake_literalref_role.run()

    assert str(expected) == str(actual)
