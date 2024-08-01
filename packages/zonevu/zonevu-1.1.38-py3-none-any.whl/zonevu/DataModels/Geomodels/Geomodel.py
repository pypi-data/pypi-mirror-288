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

from typing import Optional, ClassVar, List
from dataclasses import dataclass, field
from ..DataModel import DataModel, ChangeAgentEnum
from ..Company import Division
from ..PrimaryDataObject import PrimaryDataObject, DataObjectTypeEnum
from ..Geomodels.DataGrid import DataGrid
from ..Geomodels.Structure import Structure
from ..Strat.StratColumn import StratColumnEntry
from ..Document import Document
from datetime import datetime
from pathlib import Path
from ..Helpers import MakeIsodateOptionalField
from ...Services.Storage import Storage


@dataclass
class Geomodel(PrimaryDataObject):
    external_id: Optional[str] = None
    external_source: Optional[str] = None
    creator: Optional[str] = None
    change_agent: ChangeAgentEnum = ChangeAgentEnum.Unknown
    creation_date: Optional[datetime] = MakeIsodateOptionalField()
    last_modified_date: Optional[datetime] = MakeIsodateOptionalField()
    division: Optional[Division] = None
    strat_column: Optional[StratColumnEntry] = None
    description: Optional[str] = None
    data_grids: List[DataGrid] = field(default_factory=list[DataGrid])
    structures: List[Structure] = field(default_factory=list[Structure])
    documents: List[Document] = field(default_factory=list[Document])

    archive_dir_name: ClassVar[str] = 'geomodels'
    archive_json_filename: ClassVar[str] = 'geomodel.json'

    @property
    def full_name(self) -> str:
        return self.name

    @property
    def data_object_type(self) -> DataObjectTypeEnum:
        return DataObjectTypeEnum.Geomodel

    @property
    def archive_local_dir_path(self) -> Path:
        return Path(self.archive_dir_name) / self.safe_name

    @property
    def archive_local_file_path(self) -> Path:
        return self.archive_local_dir_path / self.archive_json_filename

    def save(self, storage: Storage) -> None:
        # Erase all files in this well folder to avoid inconsistent data
        super().save(storage)

        # Give change for specialized items to be written.
        for data_grid in self.data_grids:
            data_grid.save(self.archive_local_dir_path, storage)
        for structure in self.structures:
            structure.save(self.archive_local_dir_path, storage)

    @classmethod
    def retrieve(cls, dir_path: Path, storage: Storage) -> 'Geomodel':
        project_json_path = dir_path / cls.archive_json_filename
        json_obj = PrimaryDataObject.retrieve_json(project_json_path, storage)
        geomodel = cls.from_dict(json_obj)

        # Give change for specialized items to be read.
        for data_grid in geomodel.data_grids:
            data_grid.retrieve(dir_path, storage)
        for structure in geomodel.structures:
            structure.retrieve(dir_path, storage)

        return geomodel


@dataclass
class GeomodelEntry(DataModel):
    # Represents a ZoneVu seismic survey catalog entry Object (lightweight)
    division: Optional[Division] = None
    number: Optional[str] = None
    type: str = ''
    description: Optional[str] = None
    row_version: Optional[str] = None
    num_datasets: int = 0

    @property
    def geomodel(self) -> Geomodel:
        return Geomodel(id=self.id, name=self.name, row_version=self.row_version, description=self.description,
                        division=self.division)

