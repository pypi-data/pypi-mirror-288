"""
Tests for API ResultStatus.
"""
from http import HTTPStatus

import pytest

from bh_apistatus.result_status import(
    ResultStatus,
    make_status,
    make_500_status,
    clone_status,
)

@pytest.mark.result_status
def test_library_make_status():
    text = "I am okay..."
    status = make_status(text=text)

    assert isinstance(status, ResultStatus) == True
    assert status.code == HTTPStatus.OK.value
    assert status.text == text    
    assert status.session_id == None
    assert status.data == None
    assert status.has_data == False

    status_dict = status.as_dict()
    assert status_dict['status']['code'] == HTTPStatus.OK.value
    assert status_dict['status']['text'] == text
    assert ('session_id' not in status_dict['status']) == True
    assert ('data' not in status_dict) == True

@pytest.mark.result_status
def test_library_make_500_status():
    text = "I am not okay..."
    session_id = "7578f4d3-353a-4de6-b080-317ddbbc512f.9LJkQNW9FW7wGPukgvN-lBMeySA"
    status = make_500_status(text, session_id)

    assert isinstance(status, ResultStatus) == True
    assert status.code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert status.text == text
    assert status.session_id == session_id
    assert status.data == None
    assert status.has_data == False

    status_dict = status.as_dict()
    assert status_dict['status']['code'] == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert status_dict['status']['text'] == text
    assert status_dict['status']['session_id'] == session_id

    new_session_id = "adb3d44f-892a-4eca-9550-db319a2bedd4.nS2P-UWabbAHCsQbuLIcPG_EF38"
    status.session_id = new_session_id
    assert status.session_id == new_session_id

    status_dict = status.as_dict()
    assert status_dict['status']['session_id'] == new_session_id

@pytest.mark.result_status
def test_library_clone_status():
    text1 = "I have reported this!"
    session_id1 = "abcd efz"
    status1 = make_status(HTTPStatus.ALREADY_REPORTED.value, text1)
    status1.session_id = session_id1

    assert status1.code == HTTPStatus.ALREADY_REPORTED.value
    assert status1.text == text1
    assert status1.session_id == session_id1

    status2 = clone_status(status1)

    assert status2.code == HTTPStatus.ALREADY_REPORTED.value
    assert status2.text == text1
    assert status2.session_id == session_id1

@pytest.mark.result_status
def test_library_copy_status_info():
    """
    Als test method chainability.
    """    
    text1 = "I have reported this!"
    session_id1 = "abcd efz"
    status1 = make_status(HTTPStatus.ALREADY_REPORTED.value, text1)
    status1.session_id = session_id1

    assert status1.code == HTTPStatus.ALREADY_REPORTED.value
    assert status1.text == text1
    assert status1.session_id == session_id1

    text2 = "I am not okay!"
    session_id2 = "byk xyz"
    status2 = make_500_status(text=text2, session_id=session_id2)

    status1_itself = status1.copy_status_info(status2)

    assert status1.code == HTTPStatus.INTERNAL_SERVER_ERROR.value
    assert status1.text == text2
    assert status1.session_id == session_id2

    assert status1_itself == status1

"""
The test below to illustrate how 'data' attribute is accessed in 'status'.

Full and complete tests for data are in module:

    F:\book_keeping\tests\library\test_result_data.py
"""

person = {
    'first_name': 'Be Hai',
    'surname': 'Nguyen',
}

order = {
    'date': '2022-10-23',
    'item': 'A Book',
}

@pytest.mark.result_status
def test_library_make_status_with_data():
    text = "I am okay..."

    status = make_status(text=text, data=person, data_name='person')

    assert isinstance(status, ResultStatus) == True
    assert status.code == HTTPStatus.OK.value
    assert status.text == text    
    assert status.session_id == None
    assert status.data != None
    assert status.has_data == True
    assert status.data.person['first_name'] == 'Be Hai'
    assert status.data.person['surname'] == 'Nguyen'

    status_dict = status.as_dict()
    assert status_dict['status']['code'] == HTTPStatus.OK.value
    assert status_dict['status']['text'] == text
    assert ('session_id' not in status_dict['status']) == True
    assert ('data' in status_dict) == True

    assert status_dict['data']['person']['first_name'] == 'Be Hai'
    assert status_dict['data']['person']['surname'] == 'Nguyen'

@pytest.mark.result_status
def test_library_add_data():
    """
    Test method chainability.
    """
    status = ResultStatus()
    status_itself = status.add_data(person).add_data(order)

    assert status_itself == status

    assert hasattr(status, 'data') == True

    assert hasattr(status.data, 'first_name') == True
    assert hasattr(status.data, 'surname') == True
    assert hasattr(status.data, 'date') == True
    assert hasattr(status.data, 'item') == True

    assert status.data.first_name == 'Be Hai'
    assert status.data.surname == 'Nguyen'
    assert status.data.date == '2022-10-23'
    assert status.data.item == 'A Book'

    """
    status_itself is status.
    """
    status_dict = status_itself.as_dict()

    assert status_dict['data']['first_name'] == 'Be Hai'
    assert status_dict['data']['surname'] == 'Nguyen'
    assert status_dict['data']['date'] == '2022-10-23'
    assert status_dict['data']['item'] == 'A Book'
