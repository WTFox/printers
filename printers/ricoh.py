import base64
import xml.etree.ElementTree as ET

import requests

from . import ricoh_xml

__author__ = 'afox'


# TODO: clean up code


class LoginFailure(Exception):
    pass


class Ricoh:
    def __init__(self, host, username, password):
        self.host = host
        self.url = "http://{}/DH/udirectory".format(self.host)
        self.headers = {'content-type': 'text/xml; charset=utf-8'}
        self.soapActionUrl = 'http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory#{}'
        self.stringOut = self._connect(username, password)

        if not self.stringOut:
            raise LoginFailure

        self.user_ids = self._get_user_ids()
        self.users = self.get_users_with_details()
        self.next_index = max([int(x['index']) for x in self.users]) + 1

    def _connect(self, username, password):
        username = base64.b64encode(username.encode()).decode()
        password = base64.b64encode(password.encode()).decode()
        stringIn = "SCHEME=QkFTSUM=;UID:UserName={};PWD:Password={};PES:Encoding=gwpwes003".format(username, password)
        _xml = ricoh_xml.auth_xml.format(stringIn)
        self.headers['SOAPAction'] = self.soapActionUrl.format('startSession')

        response = requests.post(self.url, data=_xml, headers=self.headers)

        if response.ok:
            tree = ET.fromstring(response.text)
            stringOut = tree.find('{http://schemas.xmlsoap.org/soap/envelope/}Body') \
                .find('{http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory}startSessionResponse') \
                .find('stringOut').text
            return stringOut

        return False

    def disconnect(self):
        self.headers['SOAPAction'] = self.soapActionUrl.format('terminateSession')
        _xml = ricoh_xml.disconnect_xml.format(self.stringOut)
        requests.post(self.url, data=_xml, headers=self.headers)

    @staticmethod
    def _get_tagid(userid):
        starting_letter = userid[0].lower()
        trans_map = dict(
            AB=2, CD=3, EF=4, GH=5,
            IJK=6, LMN=7, OPQ=8, RST=9,
            UVW=10, XYZ=11,
        )

        for k, v in trans_map.items():
            if starting_letter in k.lower():
                return '1,{}'.format(v)

    def get_users_with_details(self):
        merged_users = [self.get_details_by_id(self.user_ids[0:50]) +
                        self.get_details_by_id(self.user_ids[50:100]) +
                        self.get_details_by_id(self.user_ids[100:])]

        return merged_users[0]

    def _get_user_ids(self):
        self.headers['SOAPAction'] = self.soapActionUrl.format('searchObjects')
        _user_ids = []

        for offset in range(0, 151, 25):
            search_options = dict(
                stringOut=self.stringOut,
                rowOffset=offset,
                rowCount='25',
                lastObjectId=''
            )

            _xml = ricoh_xml.search_xml.format(**search_options)

            try:
                response = requests.post(self.url, data=_xml, headers=self.headers)
                tree = ET.fromstring(response.text)
                results_tree = tree.find('{http://schemas.xmlsoap.org/soap/envelope/}Body') \
                    .find('{http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory}searchObjectsResponse')

                return_value = results_tree.find('returnValue').text
                row_list = results_tree.find('rowList')

            except:
                break

            if return_value == 'OK':
                for row in row_list.getchildren():
                    _user_id = row.find('item').find('propVal').text
                    if len(_user_id) < 10:
                        _user_ids.append(_user_id)

        return list(set(sorted([int(x) for x in _user_ids])))

    def get_details_by_id(self, ids):
        output = []
        ids = list(ids)
        if not len(ids):
            return []

        self.headers['SOAPAction'] = self.soapActionUrl.format('getObjectsProps')
        options = dict(
            stringOut=self.stringOut,
            objects_length=len(ids),
            objects=''.join(['<item>entry:{}</item>\n\t\t\t\t'.format(x) for x in ids])
        )
        _xml = ricoh_xml.get_object_xml.format(**options)
        response = requests.post(self.url, data=_xml, headers=self.headers)
        tree = ET.fromstring(response.text)

        usersWithDetails = tree.find('{http://schemas.xmlsoap.org/soap/envelope/}Body') \
            .find('{http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory}getObjectsPropsResponse') \
            .find('returnValue')

        for user in usersWithDetails:
            obj = {}
            for item in user.getchildren():
                obj[item.find('propName').text] = item.find('propVal').text

            output.append(obj)

        return output

    def add_user(self, userid=None, name=None, displayName=None):
        self.headers['SOAPAction'] = self.soapActionUrl.format('putObjects')

        if not all([userid, name, displayName]):
            return False

        options = dict(
            sessionId=self.stringOut,
            index=self.next_index,
            name=name,
            longName=displayName,
            auth_name=userid,
            is_destination='true',
            is_sender='false',
            mail='true',
            mail_address='{}@cbjw.net'.format(userid),
            tagId=self._get_tagid(userid),
        )

        _xml = ricoh_xml.add_user_xml.format(**options)
        response = requests.post(self.url, data=_xml, headers=self.headers)

        if not response.ok:
            print(_xml)
            print(options)
            print(response.text)

        self.next_index += 1

        return

    def delete_user(self, user_id):
        self.headers['SOAPAction'] = self.soapActionUrl.format('deleteObjects')
        options = dict(
            sessionId=self.stringOut,
            user_id=user_id
        )
        _xml = ricoh_xml.delete_user_xml.format(**options)
        response = requests.post(self.url, data=_xml, headers=self.headers)
        if not response.ok:
            print(_xml)
            print(response.text)

        return
