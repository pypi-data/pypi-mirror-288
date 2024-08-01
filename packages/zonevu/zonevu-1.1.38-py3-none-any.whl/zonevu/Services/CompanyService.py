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
#
#
#
#

from typing import Tuple, List
from .Client import Client
from ..DataModels.Company import Company, Division


class CompanyService:
    client: Client

    def __init__(self, c: Client):
        self.client = c

    def get_info(self) -> Company:
        item = self.client.get('company', None, False)
        return Company.from_dict(item)

    def get_divisions(self) -> List[Division]:
        url = "company/divisions"
        items = self.client.get_list(url)
        divisions = [Division.from_dict(w) for w in items]
        return divisions

    def get_delete_authorization(self) -> None:
        """
        Sends a 6-digit delete authorization code the caller's cell phone or email address.
        Good for 24 hours and only from the device that called this method.
        Available only if this ZoneVu account is enabled for Web API deleting.
        @return:
        """
        self.client.get('company/deleteauth')

    def confirm_delete_authorization(self, code: str) -> Tuple[bool, str]:
        """
        Confirms whether a 6-digit delete authorization code is valid for this device.
        @param code: 6-digit authorization code
        @return: true or false, and a message that is 'OK' if true, or an error message if false.
        """
        item = self.client.get_dict('company/confirmdeleteauth', {"deletecode": code})
        return item["confirmed"], item["msg"]
