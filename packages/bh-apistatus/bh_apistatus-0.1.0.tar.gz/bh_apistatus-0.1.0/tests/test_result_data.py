"""
Tests for API ResultData.
"""
from http import HTTPStatus

import pytest

from bh_apistatus.result_data import ResultData

person = {
    'first_name': 'Be Hai',
    'surname': 'Nguyen',
}

contractor = [{'CONTRACTOR_ID': 1,
  'EMAIL': 'behai_nguyen@hotmail.com',
  'GIVENNAME': 'Van Be Hai',
  'SURNAME': 'NGUYEN'}]

report = {'clientName': 'ACME IT Recruitment',
 'contractorName': 'NGUYEN Van Be Hai',
 'periodEnd': 'April 20 2003',
 'periodStart': 'April 14 2003',
 'timesheetTotal': '005 hrs 00 mins',
 'entries': [{'breakTime': '00:00',
              'chargeable': 'Yes',
              'dailyTotal': '05:00',
              'endTime': '01:00 PM',
              'periodDate': 'April 14 2003',
              'shortDayName': 'Mon',
              'startTime': '08:00 AM'},
             {'breakTime': '00:00',
              'chargeable': '',
              'dailyTotal': '00:00',
              'endTime': '00:00 PM',
              'periodDate': 'April 20 2003',
              'shortDayName': 'Sun',
              'startTime': '00:00 AM'}]}

order = {
    'date': '2022-10-23',
    'item': 'A Book',
}

order_histories = [
    {'date': '2000-12-23'},
    {'date': '2020-01-23'}
]

sale_staff = {
    'first_name': 'John',
    'surname': 'Smith',    
}    

enquiry_histories = [
    {'subject': 'Credit Card Payment', 'date': '2019-03-08'},
    {'subject': 'Missed Delivery', 'date': '2020-12-21'},
    {'subject': 'Other...', 'date': '2021-04-18'}
]

@pytest.mark.result_data
def test_library_example_1():
    data = ResultData(data=person)

    assert data.first_name == 'Be Hai'
    assert data.surname == 'Nguyen'

    data_dict = data.as_dict()
    assert data_dict['data']['first_name'] == 'Be Hai'
    assert data_dict['data']['surname'] == 'Nguyen'

@pytest.mark.result_data
def test_library_example_2():
    data = ResultData(data=contractor)

    assert (len(data) == 1)
    assert data[0]['CONTRACTOR_ID'] == 1
    assert data[0]['SURNAME'] == 'NGUYEN'

    data_dict = data.as_dict()
    assert (len(data_dict['data']) == 1)
    assert data_dict['data'][0]['CONTRACTOR_ID'] == 1
    assert data_dict['data'][0]['SURNAME'] == 'NGUYEN'

@pytest.mark.result_data
def test_library_example_3():
    data = ResultData(data=report)

    assert data.clientName == 'ACME IT Recruitment'
    assert data.timesheetTotal == '005 hrs 00 mins'
    assert len(data.entries) == 2
    assert data.entries[0]['endTime'] == '01:00 PM'
    assert data.entries[1]['endTime'] == '00:00 PM'

    data_dict = data.as_dict()
    assert data_dict['data']['clientName'] == 'ACME IT Recruitment'
    assert data_dict['data']['timesheetTotal'] == '005 hrs 00 mins'
    assert len(data_dict['data']['entries']) == 2
    assert data_dict['data']['entries'][0]['endTime'] == '01:00 PM'
    assert data_dict['data']['entries'][1]['endTime'] == '00:00 PM'

@pytest.mark.result_data
def test_library_example_4():
    data = ResultData(data=person, data_name='person')

    assert data.person['first_name'] == 'Be Hai'
    assert data.person['surname'] == 'Nguyen'

    data_dict = data.as_dict()
    assert data_dict['data']['person']['first_name'] == 'Be Hai'
    assert data_dict['data']['person']['surname'] == 'Nguyen'

@pytest.mark.result_data
def test_library_example_5():
    data = ResultData(data=contractor, data_name='contractor')

    assert data.contractor[0]['CONTRACTOR_ID'] == 1
    assert data.contractor[0]['SURNAME'] == 'NGUYEN'

    data_dict = data.as_dict()
    assert data_dict['data']['contractor'][0]['CONTRACTOR_ID'] == 1
    assert data_dict['data']['contractor'][0]['SURNAME'] == 'NGUYEN'

@pytest.mark.result_data
def test_library_example_6():
    data = ResultData(data=report, data_name='report')

    assert data.report['clientName'] == 'ACME IT Recruitment'
    assert data.report['timesheetTotal'] == '005 hrs 00 mins'
    assert len(data.report['entries']) == 2
    assert data.report['entries'][0]['endTime'] == '01:00 PM'
    assert data.report['entries'][1]['endTime'] == '00:00 PM'

    data_dict = data.as_dict()
    assert data_dict['data']['report']['clientName'] == 'ACME IT Recruitment'
    assert data_dict['data']['report']['timesheetTotal'] == '005 hrs 00 mins'
    assert len(data_dict['data']['report']['entries']) == 2
    assert data_dict['data']['report']['entries'][0]['endTime'] == '01:00 PM'
    assert data_dict['data']['report']['entries'][1]['endTime'] == '00:00 PM'

@pytest.mark.result_data
def test_library_example_7():
    customer = person

    data = ResultData(data=customer)
    data.add(data=order)

    assert data.first_name == 'Be Hai'
    assert data.surname == 'Nguyen'
    assert data.date == '2022-10-23'
    assert data.item == 'A Book'

    data_dict = data.as_dict()
    assert data_dict['data']['first_name'] == 'Be Hai'
    assert data_dict['data']['surname'] == 'Nguyen'    
    assert data_dict['data']['date'] == '2022-10-23'
    assert data_dict['data']['item'] == 'A Book'

@pytest.mark.result_data
def test_library_example_8():
    customer = person

    data = ResultData(data=customer)
    data.add(data=order)
    data.add(data=order_histories)

    assert data.first_name == 'Be Hai'
    assert data.surname == 'Nguyen'
    assert data.date == '2022-10-23'
    assert data.item == 'A Book'

    # Accessing order_histories which was stored with no attribute name.
    assert len(data) == 2
    assert data[0]['date'] == '2000-12-23'
    assert data[1]['date'] == '2020-01-23'

    data_dict = data.as_dict()
    assert data_dict['data']['first_name'] == 'Be Hai'
    assert data_dict['data']['surname'] == 'Nguyen'    
    assert data_dict['data']['date'] == '2022-10-23'
    assert data_dict['data']['item'] == 'A Book'

    # Accessing order_histories which was stored with no attribute name.
    # As a dictionary, it must have a attribute. The default is 'items'.

    assert len(data_dict['data']['items']) == 2
    assert data_dict['data']['items'][0]['date'] == '2000-12-23'
    assert data_dict['data']['items'][1]['date'] == '2020-01-23'

@pytest.mark.result_data
def test_library_example_9():
    customer = person

    data = ResultData(data=customer)
    data.add(order, 'order')
    data.add(order_histories, 'order_histories')

    assert data.first_name == 'Be Hai'
    assert data.surname == 'Nguyen'

    assert data.order['date'] == '2022-10-23'
    assert data.order['item'] == 'A Book'

    assert len(data.order_histories) == 2
    assert data.order_histories[0]['date'] == '2000-12-23'
    assert data.order_histories[1]['date'] == '2020-01-23'

    data_dict = data.as_dict()
    assert data_dict['data']['first_name'] == 'Be Hai'
    assert data_dict['data']['surname'] == 'Nguyen'    

    assert data_dict['data']['order']['date'] == '2022-10-23'
    assert data_dict['data']['order']['item'] == 'A Book'

    assert len(data_dict['data']['order_histories']) == 2
    assert data_dict['data']['order_histories'][0]['date'] == '2000-12-23'
    assert data_dict['data']['order_histories'][1]['date'] == '2020-01-23'

@pytest.mark.result_data
def test_library_example_10():
    customer = person

    data = ResultData(data=customer)
    data.add(data=sale_staff)

    assert data.first_name == 'Be Hai'
    assert data.surname == 'Nguyen'

    assert data.first_name_1 == 'John'
    assert data.surname_1 == 'Smith'

    data_dict = data.as_dict()
    assert data_dict['data']['first_name'] == 'Be Hai'
    assert data_dict['data']['surname'] == 'Nguyen'

    assert data_dict['data']['first_name_1'] == 'John'
    assert data_dict['data']['surname_1'] == 'Smith'

@pytest.mark.result_data
def test_library_example_11():
    data = ResultData(data=order_histories)
    data.add(data=enquiry_histories)

    assert len(data) == 3
    assert data[0]['subject'] == 'Credit Card Payment'
    assert data[2]['subject'] == 'Other...'

    data_dict = data.as_dict()
    assert len(data_dict['data']) == 3
    assert data_dict['data'][0]['subject'] == 'Credit Card Payment'
    assert data_dict['data'][2]['subject'] == 'Other...'

@pytest.mark.result_data
def test_library_serialise_data_01():
    data = ResultData(data=report).serialise_data()

    assert data == report    
    assert data != order_histories

    data['clientName'] == 'ACME IT Recruitment'
    data['entries'][0]['breakTime'] == '00:00'

    data = ResultData(data=order_histories).serialise_data()

    data == order_histories
    data != report

    data[0]['date'] == '2000-12-23'
    data[0]['date'] == '2020-01-23'

@pytest.mark.result_data
def test_library_serialise_data_02():
    """
    Assertain ResultData.serialise_data() return and empty  dictionary {} 
    when no data has been set yet. And no exception is raised in this case.
    """
    data = ResultData().serialise_data()

    assert data == {} 
    assert len(data) == 0