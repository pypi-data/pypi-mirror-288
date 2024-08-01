#  Copyright (c) 2024 Ubiterra Corporation. All rights reserved.
#  #
#  This ZoneVu Python SDK software is the property of Ubiterra Corporation.
#  You shall use it only in accordance with the terms of the ZoneVu Service Agreement.
#  #
#  This software is made available on PyPI for download and use. However, it is NOT open source.
#  Unauthorized copying, modification, or distribution of this software is strictly prohibited.
#  #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
#  FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#  ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
#
#

from ..DataModel import DataModel
from dataclasses import dataclass
from dataclasses_json import dataclass_json, LetterCase
from typing import Optional, ClassVar, List
from strenum import StrEnum
from ...DataModels.Completions.FracEntry import FracEntry
from ...DataModels.Completions.Stage import Stage
from ...DataModels.Completions.Plug import Plug
from dataclasses import dataclass, field
from datetime import datetime
from ...DataModels.Helpers import MakeIsodateOptionalField


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class UserParam:
    id: int = -1
    name: str = ''
    unit: str = ''


@dataclass
class Frac(FracEntry):
    """
    Represents a ZoneVu frac data object on a wellbore
    """
    #: Whether this frac is the active / starred one.
    active: bool = False
    #: Name of frac service company
    service_company: str = ''
    #: Frac fleet id or name
    fleet: str = ''
    #: Frac job type
    job_type: str = ''
    #: Frac system used
    frac_system: str = ''
    #: Fluid system used
    fluid_system: str = ''
    #: Name of user who created this frac
    creator: str = ''
    #: System id of geosteering interpretation associated with this frac (if any)
    interpretation_id: Optional[int] = None
    #: List of definitions of user defined frac attributes
    user_param_defs: List[Optional[UserParam]] = field(default_factory=list[Optional[UserParam]])
    #: List of stages of this frac
    stages: List[Stage] = field(default_factory=list[Stage])
    #: List of Extra well log curves from target wellbore to included in frac table.
    extra_curve_ids: List[int] = field(default_factory=list[int])
    #: Date and time frac was last modified
    last_modified_date: Optional[datetime] = MakeIsodateOptionalField()
    #: Name of user who last modified this frac
    last_modified_by_name: str = ''

    def copy_ids_from(self, source: DataModel):
        super().copy_ids_from(source)
        if isinstance(source, Frac):
            DataModel.merge_lists(self.stages, source.stages)



