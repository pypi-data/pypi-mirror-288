import urllib.parse

import requests

from epic_py.domain.pid import Pid


class EpicAPI:

    def __init__(self, host: str, username: str = None, password: str = None):
        """
        Initialize the object with provided host and credentials.

        :param host: ePIC API host.
        :type host: str
        :param username: ePIC API username.
        :type username: str
        :param password: ePIC API password.
        :type password: str
        """
        self._host = host
        self._username = username
        self._password = password

    def get(self, pid_str: str) -> Pid:
        """
        Resolve a PID.

        :param pid_str: PID to be resolved.
        :type pid_str: str
        :return: if the credential is provided, all information will be returned.
        Otherwise, only public readable values are returned.
        """
        encoded_pid = urllib.parse.quote(pid_str)
        url = f'{self._host}/handles/{encoded_pid}'
        if self._username is not None and self._password is not None:
            response = requests.get(url, auth=(self._username, self._password))
        else:
            response = requests.get(url)
        response.raise_for_status()

        pid = Pid(data=response.json())
        pid.pid_str = pid_str

        return pid

    def create_or_update(self, pid: Pid) -> Pid:
        """
        Create a PID if it does not exist yet. Update it otherwise. In case of update, the content of the old PID
        will be overwritten.

        :param pid: the PID to be created or updated
        :type pid: Pid
        :return: the created or updated PID.
        """
        encoded_prefix = urllib.parse.quote(pid.prefix)
        payload_json = pid.dict(exclude_unset=True)['data']

        # Make a PUT request to create or update a PID with the specified suffix
        suffix = pid.suffix
        if suffix is not None:
            encoded_suffix = urllib.parse.quote(suffix)
            url = f'{self._host}/handles/{encoded_prefix}/{encoded_suffix}'
            response = requests.put(url, json=payload_json, auth=(self._username, self._password))
        else:
            # Make a POST request to create a PID with an auto-generated suffix
            url = f'{self._host}/handles/{encoded_prefix}'
            response = requests.post(url, json=payload_json, auth=(self._username, self._password))

        response.raise_for_status()
        status_code = response.status_code

        # 201-CREATED. Get the PID string from the response
        if status_code == 201:
            content = response.json()
            pid.pid_str = content['handle']

        return pid

    def create(self, pid: Pid) -> Pid:
        """
        Create a PID. If it already exists, an error will be thrown.

        :param pid: the content of the PID.
        :type pid: Pid
        :return: the newly created PID.
        """
        encoded_prefix = urllib.parse.quote(pid.prefix)
        payload_json = pid.dict(exclude_unset=True)['data']

        # Make a PUT request to create a PID with the specified suffix
        suffix = pid.suffix
        if suffix is not None:
            encoded_suffix = urllib.parse.quote(suffix)
            url = f'{self._host}/handles/{encoded_prefix}/{encoded_suffix}'

            # Make sure that the PID is only created if it hasn't been created before
            headers = {
                'If-None-Match': '*'
            }
            response = requests.put(url, json=payload_json, headers=headers, auth=(self._username, self._password))
        else:
            # Make a POST request to create a PID with an auto-generated suffix
            url = f'{self._host}/handles/{encoded_prefix}'
            response = requests.post(url, json=payload_json, auth=(self._username, self._password))

        response.raise_for_status()
        content = response.json()
        pid.pid_str = content['handle']
        return pid

    def update(self, pid: Pid) -> Pid:
        """
        Update the PID. If the PID does not exist yet, an error will be thrown.

        :param pid: the PID to be updated.
        :type pid: str
        :param pid: new content of the PID. This will overwrite the old one.
        :type pid: Pid
        :return: the updated PID
        """
        encoded_pid = urllib.parse.quote(pid.pid_str)
        payload_json = pid.dict(exclude_unset=True)['data']
        url = f'{self._host}/handles/{encoded_pid}'

        # Make sure that the PID is only updated if it exists
        headers = {
            'If-Match': '*'
        }
        response = requests.put(url, json=payload_json, headers=headers, auth=(self._username, self._password))

        response.raise_for_status()
        content = response.json()
        pid.pid_str = content['handle']
        return pid

    def delete(self, pid: str) -> None:
        """
        Delete a PID. If the PID does not exist, an error will be thrown.

        :param pid: PID to be deleted.
        :type pid: str
        :return:
        """
        encoded_pid = urllib.parse.quote(pid)
        url = f'{self._host}/handles/{encoded_pid}'
        response = requests.delete(url, auth=(self._username, self._password))
        response.raise_for_status()
