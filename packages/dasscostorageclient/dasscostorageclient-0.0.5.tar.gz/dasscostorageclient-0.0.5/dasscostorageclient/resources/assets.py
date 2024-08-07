from typing import List
from .models.specimen import SpecimenModel
from ..utils import *
from pydantic import TypeAdapter, Field, BaseModel
from datetime import datetime
from .models.httpinfo import HTTPInfoModel


class AssetModel(BaseModel):
    pid: str | None = Field(alias='asset_pid')
    guid: str = Field(alias='asset_guid')
    status: str
    multi_specimen: bool
    specimens: list[SpecimenModel]
    funding: str | None
    subject: str | None
    payload_type: str | None
    file_formats: list[str]
    asset_locked: bool
    restricted_access: list[str]
    institution: str
    collection: str
    pipeline: str
    digitiser: str | None
    parent_guid: str | None
    audited: bool
    internal_status: str
    tags: dict | None
    http_info: HTTPInfoModel | None = Field(alias='httpInfo')


class EventModel(BaseModel):
    user: str | None
    timestamp: datetime = Field(alias="timeStamp")
    event: str
    workstation: str
    pipeline: str


class AssetStatus(BaseModel):
    guid: str = Field(alias='asset_guid')
    parent_guid: str | None
    error_timestamp: datetime | None
    status: str
    error_message: str | None
    share_allocation_mb: int | None


class Assets:

    def __init__(self, access_token):
        self.access_token = access_token

    def get(self, guid: str):
        """
        Gets the metadata of the given asset

        Args:
            guid (str): The guid of the asset to be retrieved

        Returns:
            An Asset object that contains the metadata
        """
        res = send_request(
            RequestMethod.GET,
            self.access_token,
            f"/v1/assetmetadata/{guid}")

        return {
            'data': AssetModel.model_validate(res.json()),
            'status_code': res.status_code
        }

    def create(self, body: dict, allocation_mb: int):
        """
        Creates a new asset

        Args:
            body (dict): The metadata of the new asset
            allocation_mb (int): The amount of storage allocated for the new asset

        Returns:
            An Asset object that contains the metadata of the created asset
        """
        res = send_request(
            RequestMethod.POST,
            self.access_token,
            f"/v1/assetmetadata?allocation_mb={allocation_mb}",
            body)

        return {
            'data': AssetModel.model_validate(res.json()),
            'status_code': res.status_code
        }

    def update(self, guid: str, body: dict):
        """
        Updates the asset with the given guid

        Args:
            guid (str): The guid of the asset to be updated
            body (dict): The metadata to be updated in the given asset

        Returns:
            An Asset object that contains the metadata of the updated asset
        """
        res = send_request(
            RequestMethod.PUT,
            self.access_token,
            f"/v1/assetmetadata/{guid}",
            body)

        return {
            'data': AssetModel.model_validate(res.json()),
            'status_code': res.status_code
        }

    def list_events(self, guid: str):
        """
        Lists the events of the given asset

        Args:
            guid (str): The guid of the asset

        Returns:
            A list of Event objects
        """
        res = send_request(
            RequestMethod.GET,
            self.access_token,
            f"/v1/assetmetadata/{guid}/events")

        ta = TypeAdapter(List[EventModel])

        return {
            'data': ta.validate_python(res.json()),
            'status_code': res.status_code
        }

    def get_status(self, guid: str):
        res = send_request(
            RequestMethod.GET,
            self.access_token,
            f"/v1/assets/status/{guid}")

        return {
            'data': AssetStatus.model_validate(res.json()),
            'status_code': res.status_code
        }

    def list_in_progress(self, only_failed=False):
        res = send_request(
            RequestMethod.GET,
            self.access_token,
            f"/v1/assets/inprogress?onlyFailed={only_failed}")

        ta = TypeAdapter(List[AssetStatus])

        return {
            'data': ta.validate_python(res.json()),
            'status_code': res.status_code
        }


