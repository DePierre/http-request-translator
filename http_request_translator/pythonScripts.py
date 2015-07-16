#!/usr/bin/python

from urllib import quote
from util import get_url, check_valid_url
import sys

try:
    from termcolor import colored
except ImportError:
    print "Dependency of the library 'termcolor' not satisfied. \
    Do $pip install termcolor to install the library :-) "
    sys.exit(0)


def generate_script(header_dict, details_dict, searchString=None):
    url = get_url(header_dict['Host'])
    if not check_valid_url(url):
        print(
            "Please enter a valid URL with correct domain name and try again ")
        sys.exit(0)

    if details_dict['data']:
        details_dict['data'] = '"' + str(details_dict['data']) + '"'

    encoding_list = ['HEAD', 'OPTIONS', 'GET']

    if details_dict['data'] and (details_dict['method'].strip()
                                 in encoding_list):
        print "Encoding URL"
        encoded_data = quote(details_dict['data'], '')
        url = url + encoded_data
        header_dict['Host'] = url
        details_dict['data'] = None

    if searchString:
        try:
            if 'proxy' not in details_dict:
                skeleton_code = '''\
#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient
from termcolor import colored
import re

def main():
    headers, url, method = ''' + str(header_dict) + ''', "''' + url + '''" , "''' + details_dict['method'].strip() + '''"
    body = ''' + str(details_dict['data']) + '''
    request_object = HTTPRequest(url, method=method,headers=headers, body=body, allow_nonstandard_methods=True)
    response_header = HTTPClient().fetch(request_object).headers
    match = re.findall(r"''' + searchString + '''", str(response_header))
    for x in range(0, len(match)) :
        replace_string = colored(match[x], 'green')
        response_header = re.sub(match[x], replace_string, str(response_header))
    print response_header

    if __name__ == '__main__':
        main()

                '''
            else:
                skeleton_code = '''\
#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient
from termcolor import colored
import re


def main():

    headers, url, method = ''' + str(header_dict) + ''', "''' + url +\
                    '''" , "''' + details_dict['method'].strip() + '''"
    proxy_host, proxy_port = "''' + details_dict['proxy'].split(':')[0].strip() + \
                    '''", "''' + details_dict['proxy'].split(':')[1].strip() + '''"
    body = ''' + str(details_dict['data']) + '''
    request_object = HTTPRequest(url, method=method, headers=headers, proxy_host=proxy_host,\
        proxy_port=proxy_port, body=body, allow_nonstandard_methods=True)
    response_header = HTTPClient().fetch(request_object).headers
    for x in range(0, len(match)) :
        replace_string = colored(match[x], 'green')
        response_header = re.sub(match[x], replace_string, str(response_header))
    print response_header

if __name__ == '__main__':
    main()
                '''

        except IndexError:
            print "You haven't given the port Number"
        else:
            print skeleton_code

    else:
        try:
            if 'proxy' not in details_dict:
                skeleton_code = '''\
#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient

def main():
    headers, url, method = ''' + str(header_dict) + ''', "''' + url + '''" , "''' + details_dict['method'].strip() + '''"
    body = ''' + str(details_dict['data']) + '''
    request_object = HTTPRequest(url, method=method,headers=headers, body=body, allow_nonstandard_methods=True)
    response_header = HTTPClient().fetch(request_object).headers
    print response_header

if __name__ == '__main__':
    main()
                '''

            else:
                skeleton_code = '''\
#!/usr/bin/python
from tornado.httpclient import HTTPRequest, HTTPClient


def main():

    headers, url, method = ''' + str(header_dict) + ''', "''' + url +\
                    '''" , "''' + details_dict['method'].strip() + '''"
    proxy_host, proxy_port = "''' + details_dict['proxy'].split(':')[0].strip() +\
                    '''", "''' + details_dict['proxy'].split(':')[1].strip() + '''"
    body = ''' + str(details_dict['data']) + '''
    request_object = HTTPRequest(url, method=method, headers=headers,\
        proxy_host=proxy_host, proxy_port=proxy_port, body=body, allow_nonstandard_methods=True)
    return HTTPClient().fetch(request_object).headers


if __name__ == '__main__':
    main()
                '''

        except IndexError:
            print "You haven't given the port Number"

        else:
            print(skeleton_code)
