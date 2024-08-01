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

from typing import Optional, Union
from dataclasses import dataclass, field
from dataclasses_json import config
from ...DataModels.DataModel import DataModel
from datetime import datetime
from ...DataModels.Helpers import MakeIsodateOptionalField


@dataclass
class Note(DataModel):
    md: float = field(default=0.0, metadata=config(field_name="MD"))
    owner: str = ''
    creation_time: datetime = MakeIsodateOptionalField()
    wellbore_id: int = -1
    description: Optional[str] = None
    category: Optional[str] = None
    category_id: Optional[int] = None
    interpretation: Optional[str] = None
    interpretation_id: Optional[int] = None
