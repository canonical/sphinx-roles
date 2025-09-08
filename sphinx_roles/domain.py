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
"""Add a custom domain to support monospaced internal links."""

from typing import cast

from docutils.nodes import Element, reference
from sphinx.addnodes import pending_xref
from sphinx.builders import Builder
from sphinx.domains.std import StandardDomain
from sphinx.environment import BuildEnvironment
from typing_extensions import override


class LiteralrefDomain(StandardDomain):
    """Custom domain for the :literalref: role."""

    name: str = "lrd"

    @override
    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: pending_xref,
        contnode: Element,
    ) -> reference | None:
        """Replace the resolved node's child with the children assigned to the pending reference node.

        By default, Sphinx's standard domain
        disregards the type of the pending node's children and places their
        contents into an inline node.
        """
        if node.get("refdomain") != "lrd":
            return None

        resolved_node = super().resolve_xref(
            env, fromdocname, builder, typ, target, node, contnode
        )  # resolve the reference using the standard domain

        if (
            resolved_node
            and hasattr(resolved_node, "children")
            and hasattr(node, "children")
        ):  # replace the child node from ``std`` with the original children
            resolved_node.children = node.children

        return cast(reference, resolved_node)
