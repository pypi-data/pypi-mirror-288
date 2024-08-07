import string
import random
from hashlib import md5
from urllib.parse import urljoin, urlparse

import requests


def get_hash(s):
    return md5(s.encode('utf-8')).hexdigest()


class TempMail(object):
    """
    API Wrapper for service which provides temporary email address. 
    The subset of methods are only implemented.
    """

    def __init__(self, api_key, api_base_url='https://privatix-temp-mail-v1.p.rapidapi.com'):
        self.__api_base_url = api_base_url
        self.__api_key = api_key
        self.__avaiable_domains = None


    def __make_headers(self):
            netloc = urlparse(self.__api_base_url).netloc
            return {
                'x-rapidapi-host': netloc,
                'x-rapidapi-key': self.__api_key
            }            


    def available_domains(self):
        """
        Return list of available domains for use in email address.
        """
        if self.__avaiable_domains is None:
            url = urljoin(self.__api_base_url, 'request/domains')
            req = requests.get(url, headers=self.__make_headers())
            self.__avaiable_domains = req.json()

        return self.__avaiable_domains
        

    def make_user_name(self):
        """
        Generate string for email address login.
        """
        alphabet = string.ascii_lowercase + string.digits
        return ''.join(random.choice(alphabet) for _ in range(8))


    def make_email_address(self):
        """
        Return full email address from login and domain from params in class
        initialization or generate new.
        """
        username = self.make_user_name()
        domain = random.choice(self.available_domains())
        return f'{username}{domain}'


    def get_message_list(self, email):
        """
        Return list of emails in given email address
        or dict with `error` key if mail box is empty.

        :param email: (optional) email address.
        :param email_hash: (optional) md5 hash from email address.
        """

        url = urljoin(self.__api_base_url, f'request/mail/id/{get_hash(email)}')
        req = requests.get(url, headers=self.__make_headers())
        return req.json()


    def delete_message(self, email, message_id):
        """
        Delete a given email in a given email address

        :param email: (optional) email address.
        :param email_hash: (optional) md5 hash from email address.
        """

        url = urljoin(self.__api_base_url, f'request/delete/id/{{{message_id}}}')
        print(url)
        req = requests.get(url, headers=self.__make_headers())
        return req.json()
