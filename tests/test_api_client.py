import pytest
from unittest.mock import Mock, patch
from src.api_client import SpaceXAPIClient

@pytest.fixture
def api_client():
    return SpaceXAPIClient()

def test_api_client_initialization(api_client):
    assert api_client.BASE_URL == "https://api.spacexdata.com/v4"
    assert 'User-Agent' in api_client.session.headers

@patch('src.api_client.requests.Session.get')
def test_make_request_success(mock_get, api_client):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'test': 'data'}
    mock_get.return_value = mock_response
    
    result = api_client._make_request('test')
    
    assert result == {'test': 'data'}
    mock_get.assert_called_once_with('https://api.spacexdata.com/v4/test', params=None, timeout=10)

@patch('src.api_client.requests.Session.get')
def test_make_request_failure(mock_get, api_client):
    mock_get.side_effect = Exception('API error')
    
    with pytest.raises(Exception):
        api_client._make_request('test')

@patch('src.api_client.SpaceXAPIClient._make_request')
def test_get_all_launches(mock_make_request, api_client):
    mock_data = [{
        'id': 'test1', 
        'flight_number': 1,
        'name': 'Test Launch',
        'date_utc': '2023-01-01T00:00:00.000Z',
        'date_unix': 1672531200,
        'date_local': '2023-01-01T00:00:00-05:00',
        'date_precision': 'hour',
        'rocket': 'falcon9',
        'success': True,
        'upcoming': False,
        'launchpad': 'ksc_lc_39a',
        'extra_fields': {}
    }]
    mock_make_request.return_value = mock_data
    
    launches = api_client.get_all_launches()
    
    assert len(launches) == 1
    assert launches[0].id == 'test1'
    mock_make_request.assert_called_once_with('launches')

@patch('src.api_client.SpaceXAPIClient._make_request')
def test_get_launch_by_id(mock_make_request, api_client):
    mock_data = {
        'id': 'test1', 
        'flight_number': 1,
        'name': 'Test Launch',
        'date_utc': '2023-01-01T00:00:00.000Z',
        'date_unix': 1672531200,
        'date_local': '2023-01-01T00:00:00-05:00',
        'date_precision': 'hour',
        'rocket': 'falcon9',
        'success': True,
        'upcoming': False,
        'launchpad': 'ksc_lc_39a',
        'extra_fields': {}
    }
    mock_make_request.return_value = mock_data
    
    launch = api_client.get_launch_by_id('test1')
    
    assert launch.id == 'test1'
    mock_make_request.assert_called_once_with('launches/test1')