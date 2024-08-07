import pytest
from .dassco_test_client import client

ASSET_GUID = "tb-asset-002"


@pytest.mark.skip(reason="No endpoint for clean up")
def test_can_create_asset():
    body = {
        "asset_pid": "asdf-12346-3333-100a21",
        "asset_guid": "test_asset",
        "funding": "some funding",
        "subject": "folder",
        "institution": "test-institution",
        "pipeline": "ti-p1",
        "collection": "test-collection",
        "workstation": "ti-ws-01",
        "status": "WORKING_COPY",
    }
    res = client.assets.create(body, 1)
    status_code = res.get('status_code')
    asset = res.get('data')
    assert status_code == 200
    assert asset.guid == 'test_asset'
    assert asset.http_info.allocated_storage_mb == 1


def test_can_get_asset():
    res = client.assets.get(ASSET_GUID)
    status_code = res.get('status_code')
    asset = res.get('data')
    assert status_code == 200
    assert asset.guid == ASSET_GUID


def test_can_update_asset():
    # TODO: Replace asset_guid with the created asset guid from the first test when DELETE endpoint is available
    body = {
        'funding': 'test funding',
        'subject': 'test subject',
        'updateUser': 'Test user',  # Required
        'institution': 'test-institution',  # Required
        'pipeline': 'ti-p1',  # Required
        'collection': 'test-collection',  # Required
        'workstation': 'ti-ws-01',  # Required
        'status': 'WORKING_COPY'  # Required
    }
    res = client.assets.update(ASSET_GUID, body)
    status_code = res.get('status_code')
    asset = res.get('data')
    assert status_code == 200
    assert asset.funding == 'test funding'
    assert asset.subject == 'test subject'


def test_can_list_events():
    res = client.assets.list_events(ASSET_GUID)
    status_code = res.get('status_code')
    events = res.get('data')
    assert status_code == 200
    assert isinstance(events, list)
