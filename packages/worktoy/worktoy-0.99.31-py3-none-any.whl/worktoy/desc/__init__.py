"""The 'worktoy.desc' implements the descriptor protocol with lazy
instantiation. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._owner_instance import THIS, SCOPE
from ._abstract_descriptor import AbstractDescriptor
from ._attri_box import AttriBox
from ._empty_field import EmptyField
