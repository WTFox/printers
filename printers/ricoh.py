import base64
import xml.etree.ElementTree as ET
from itertools import islice
from collections import namedtuple

import requests

from . import ricoh_xml

__author__ = 'afox'


# TODO: clean up code


class LoginFailure(Exception):
    pass


class FatalError(Exception):
    pass


class Ricoh:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.url = "http://{}/DH/udirectory".format(self.host)

    def __enter__(self):
        self.stringOut = self._connect(self.username, self.password)
        if not self.stringOut:
            raise LoginFailure

        self.user_ids = self._get_user_ids()
        self.users = self.get_details_by_id(self.user_ids)
        if len(self.users) == 0:
            totalusers = 0
        else:
            totalusers = max([int(x.index) for x in self.users])
        self.next_index = totalusers + 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def __len__(self):
        return len(self.users)

    def __iter__(self):
        for _user in self.users:
            yield _user

    def __str__(self):
        return "There are {} users in {}".format(len(self), self.host)

    def __repr__(self):
        return '<Ricoh(%s)> at %s' % (self.host, id(self))

    def _connect(self, username, password):
        username = base64.b64encode(username.encode()).decode()
        password = base64.b64encode(password.encode()).decode()
        encoding = ("gwpwes003","")[bool(password)] #Encoding has to be empty if password
        stringIn = "SCHEME=QkFTSUM=;UID:UserName={};PWD:Password={};PES:Encoding={}".format(username, password, encoding)
        result = self._post_to_copier('startSession', {'stringIn': stringIn}, ricoh_xml.auth_xml)
        if result['success']:
            stringOut = result['tree'].find('{http://schemas.xmlsoap.org/soap/envelope/}Body') \
                .find('{http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory}startSessionResponse') \
                .find('stringOut').text
            return stringOut

        return False

    def disconnect(self):
        self._post_to_copier('terminateSession', dict(sessionId=self.stringOut), ricoh_xml.disconnect_xml)

    @staticmethod
    def _get_tagid(userid):
        starting_letter = userid[0].lower()
        trans_map = dict(
            AB=2, CD=3, EF=4,
            GH=5, IJK=6, LMN=7,
            OPQ=8, RST=9, UVW=10,
            XYZ=11,
        )

        for k, v in trans_map.items():
            if starting_letter in k.lower():
                return '1,{}'.format(v)

    @staticmethod
    def _get_soap_header(action):
        headers = {'content-type': 'text/xml; charset=utf-8',
                   'SOAPAction': 'http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory#{}'.format(action)}
        return headers

    @staticmethod
    def _grouper(n, iterable):
        it = iter(iterable)
        while True:
            chunk = tuple(islice(it, n))
            if not chunk:
                return
            yield chunk

    def _post_to_copier(self, action, options, xml):
        try:
            headers = self._get_soap_header(action)
            xml = xml.format(**options)
            response = requests.post(self.url, data=xml, headers=headers)
            tree = ET.fromstring(response.text)

            return dict(success=response.ok,
                        response=response.text,
                        tree=tree,
                        sent_xml=xml,
                        sent_options=options)
        except:
            return dict(success=False)

    def _get_user_ids(self):
        _user_ids = []
        search_options = dict(
            stringOut=self.stringOut,
            rowOffset=0,
            rowCount='25',
            lastObjectId=''
        )

        result = self._post_to_copier('searchObjects', search_options, ricoh_xml.search_xml)
        if result['success']:
            return_length = result['tree'].find('{http://schemas.xmlsoap.org/soap/envelope/}Body') \
                .find('{http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory}searchObjectsResponse') \
                .find('numOfResults').text

            for offset in range(0, int(return_length) + 25, 25):
                search_options = dict(
                    stringOut=self.stringOut,
                    rowOffset=offset,
                    rowCount='25',
                    lastObjectId=''
                )
                result = self._post_to_copier('searchObjects', search_options, ricoh_xml.search_xml)
                try:
                    row_list = result['tree'].find('{http://schemas.xmlsoap.org/soap/envelope/}Body') \
                        .find('{http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory}searchObjectsResponse') \
                        .find('rowList').getchildren()

                    for row in row_list:
                        _user_id = row.find('item').find('propVal').text
                        if len(_user_id) < 10:
                            _user_ids.append(_user_id)

                except AttributeError:
                    pass

        return list(set(sorted([int(x) for x in _user_ids])))

    def get_details_by_id(self, ids):
        User = namedtuple('User', ['tagId', 'id', 'index', 'mailaddress', 'name', 'isDestination', 'mailisDirectSMTP',
                                   'longName', 'mail', 'isSender', 'entryType', 'mailparameter'])
        output = []
        ids = list(ids)

        if not len(ids):
            return []

        for chunk in self._grouper(50, ids):
            search_options = dict(
                stringOut=self.stringOut,
                objects_length=len(chunk),
                objects=''.join(['<item>entry:{}</item>\n\t\t\t\t'.format(x) for x in chunk])
            )

            result = self._post_to_copier('getObjectsProps', search_options, ricoh_xml.get_object_xml)
            if not result['success']:
                self.disconnect()
                raise FatalError

            users_with_details = result['tree'].find('{http://schemas.xmlsoap.org/soap/envelope/}Body') \
                .find('{http://www.ricoh.co.jp/xmlns/soap/rdh/udirectory}getObjectsPropsResponse') \
                .find('returnValue')

            for user in users_with_details:
                obj = {}
                for item in user.getchildren():
                    obj[item.find('propName').text.replace(':', '')] = item.find('propVal').text

                User.__new__.__defaults__ = ('',) * len(User._fields)
                userObj = User(**obj)
                output.append(userObj)

        return output

    def add_user(self, userid=None, name=None, displayName=None, email=None, path=None):
        #if not all([userid, name, displayName, email]):
        if not (userid and name): #only userid and name are required, you could leave blank other fields
            return False
        if path==None:
            is_path = 'false'
        else:
            is_path = 'true'
        options = dict(
            sessionId=self.stringOut,
            index=self.next_index,
            name=name,
            longName=displayName,
            auth_name=userid,
            is_destination='true',
            is_sender='false',
            mail='true',
            mail_address=email,
            tagId=self._get_tagid(userid), #please check, userid is USER CODE and MUST be only a integer value
            remoteFolder=is_path,
            remoteFolder_path=path
        )

        result = self._post_to_copier('putObjects', options, ricoh_xml.add_user_xml)
        if not result['success']:
            self.disconnect()
            raise FatalError

        self.next_index += 1

        return

    def delete_user(self, user_id):
        options = dict(
            sessionId=self.stringOut,
            user_id=user_id
        )
        result = self._post_to_copier('deleteObjects', options, ricoh_xml.delete_user_xml)
        if not result['success']:
            self.disconnect()
            raise FatalError

        return
