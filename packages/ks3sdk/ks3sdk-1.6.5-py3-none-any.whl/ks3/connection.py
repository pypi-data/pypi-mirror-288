# coding:utf-8

#  This software code is made available without warranties of any
#  kind.  You may copy, display, modify and redistribute the software
#  code either by itself or as incorporated into your code; provided that
#  you do not remove any proprietary notices. Your use of this software
#  code is at your own risk.
import json
import os
import time
import xml.sax

from ks3 import auth
from ks3 import handler
from ks3 import utils
from ks3.bucket import Bucket, BucketLocation
from ks3.exception import S3ResponseError, S3CreateError, KS3ClientError, KS3ResponseError
from ks3.http import make_request
from ks3.provider import Provider
from ks3.resultset import ResultSet

try:
    import urllib.parse as parse  # for Python 3
except ImportError:
    import urllib as parse  # for Python 2


def check_lowercase_bucketname(n):
    """
    Bucket names must not contain uppercase characters. We check for
    this by appending a lowercase character and testing with islower().
    Note this also covers cases like numeric bucket names with dashes.

    >>> check_lowercase_bucketname("Aaaa")
    Traceback (most recent call last):
    ...
    BotoClientError: S3Error: Bucket names cannot contain upper-case
    characters when using either the sub-domain or virtual hosting calling
    format.

    >>> check_lowercase_bucketname("1234-5678-9123")
    True
    >>> check_lowercase_bucketname("abcdefg1234")
    True
    """
    if not (n + 'a').islower():
        raise KS3ClientError("Bucket names cannot contain upper-case " \
                             "characters when using either the sub-domain or virtual " \
                             "hosting calling format.")
    return True


class _CallingFormat(object):

    def get_bucket_server(self, server, bucket):
        return ''

    def build_url_base(self, connection, protocol, server, bucket, key=''):
        url_base = '%s://' % protocol
        url_base += self.build_host(server, bucket)
        url_base += connection.get_path(self.build_path_base(bucket, key))
        return url_base

    def build_host(self, server, bucket):
        if bucket == '':
            return server
        else:
            return self.get_bucket_server(server, bucket)

    def build_auth_path(self, bucket, key=''):
        key = utils.get_utf8_value(key)
        path = ''
        if bucket != '':
            path = '/' + bucket
        buf = path + '/%s' % parse.quote(key)
        buf = buf.replace('//', '/%2F')
        return buf

    def build_path_base(self, bucket, key=''):
        key = utils.get_utf8_value(key)
        buf = '/%s' % parse.quote(key)
        buf = buf.replace('//', '/%2F')
        return buf


class OrdinaryCallingFormat(_CallingFormat):

    def get_bucket_server(self, server, bucket):
        return server

    def build_path_base(self, bucket, key=''):
        key = utils.get_utf8_value(key)
        path_base = '/'
        if bucket:
            path_base += "%s/" % bucket
        return path_base + parse.quote(key)


class SubdomainCallingFormat(_CallingFormat):

    def get_bucket_server(self, server, bucket):
        return '%s.%s' % (bucket, server)


class Connection(object):
    QueryString = 'Signature=%s&Expires=%d&KSSAccessKeyId=%s'

    def __init__(self, access_key_id, access_key_secret, host="",
                 port=80, provider='kss', security_token=None, profile_name=None, path='/',
                 is_secure=False, debug=0, calling_format=SubdomainCallingFormat, domain_mode=False,
                 local_encrypt=False, local_key_path="", timeout=10, ua_addon='', enable_crc=True):
        """
        :param access_key_id: 金山云提供的ACCESS KEY ID
        :param access_key_secret: 金山云提供的SECRET KEY ID
        :param host: 请参考官网API文档说明中的Region定义(https://docs.ksyun.com/read/latest/65/_book/index.html)
        :param port: 请求端口，默认80
        :param is_secure: 是否启用HTTPS，True:启用  False:关闭
        :param domain_mode: 是否使用自定义域名访问，True:是 False:否
        :param local_encrypt: 是否启用本地加密， True:是 False:否，默认False，如选是，需要配置本地密钥路径
        :param enable_crc: 是否启用crc64校验，True:是 False:否，默认True
        """
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.is_secure = is_secure
        self.host = host
        self.port = port
        self.debug = debug
        self.path = path
        self.calling_format = calling_format()
        self.domain_mode = domain_mode
        self.local_encrypt = local_encrypt
        self.key = ""
        self.timeout = timeout
        self.ua_addon = ua_addon
        self.enable_crc = enable_crc
        if (self.is_secure):
            self.protocol = 'https'
            if self.port == 80:
                self.port = 443
        else:
            self.protocol = 'http'

        if isinstance(provider, Provider):
            # Allow overriding Provider
            self.provider = provider
        else:
            self._provider_type = provider
            self.provider = Provider(self._provider_type,
                                     access_key_id,
                                     access_key_secret,
                                     security_token,
                                     profile_name)

        # Allow config file to override default host, port, and host header.
        if self.provider.host:
            self.host = self.provider.host
        if self.provider.port:
            self.port = self.provider.port
        if self.provider.host_header:
            self.host_header = self.provider.host_header
        assert self.host
        if self.local_encrypt:
            self.load_key(local_key_path)

    def load_key(self, path):
        error_msg = "In local_encrypt mode, we need you to indicate the location of your private key. Set value for 'local_key_path' while initiate connection."
        assert path, error_msg
        with open(path, 'rb') as ak_file:
            assert os.path.getsize(path), "The key file should not be empty"
            content = ak_file.read()
            assert len(content.strip()) == 16, "The key's length should be 16"
            self.key = content.strip()

    def make_request(self, method, bucket="", key="", data="",
                     headers=None, query_args=None, metadata=None, timeout=10):
        if not headers:
            headers = {}
        if not query_args:
            query_args = {}
        if not metadata:
            metadata = {}
        timeout = self.timeout
        resp = make_request(self.host, self.port, self.access_key_id,
                            self.access_key_secret, bucket, key,
                            query_args, headers, data, metadata, method=method, is_secure=self.is_secure, domain_mode=self.domain_mode,
                            timeout=timeout, ua_addon=self.ua_addon)

        return resp

    def get_all_buckets(self, headers=None, project_ids=None):
        query_args = {}
        if project_ids is not None:
            query_args = {
                "projectIds": project_ids
            }
        response = self.make_request('GET', headers=headers, query_args=query_args)
        body = response.read()
        if response.status > 300:
            raise S3ResponseError(response.status, response.reason, body)
        rs = ResultSet([('Bucket', Bucket)])
        h = handler.XmlHandler(rs, self)
        if not isinstance(body, bytes):
            body = body.encode('utf-8')
        xml.sax.parseString(body, h)
        return rs

    def get_bucket(self, bucket_name, headers=None):
        return Bucket(self, bucket_name)

    def head_bucket(self, bucket_name, headers=None):
        response = self.make_request('HEAD', bucket_name)
        body = response.read()
        if response.status == 200:
            return response.headers
        else:
            raise S3ResponseError(response.status, response.reason, body)

    def get_bucket_location(self, bucket_name):
        response = self.make_request('GET', bucket_name, query_args='location')
        body = response.read()
        if response.status == 200:
            loc = BucketLocation()
            h = handler.XmlHandler(loc, self)
            xml.sax.parseString(body, h)
            return loc.location
        else:
            raise S3ResponseError(response.status, response.reason, body)

    def create_bucket(self, bucket_name, headers=None, project_id=None,
                      location=None, policy=None):
        check_lowercase_bucketname(bucket_name)

        if policy:
            if headers:
                headers[self.provider.acl_header] = policy
            else:
                headers = {self.provider.acl_header: policy}
        if location == None:
            data = ''
        else:
            data = '<CreateBucketConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><LocationConstraint>' + \
                   location + '</LocationConstraint></CreateBucketConfiguration>'

        query_args = {}
        if project_id is not None:
            query_args = {
                "projectId": project_id
            }
        response = self.make_request('PUT', bucket_name, headers=headers, query_args=query_args,
                                     data=data)
        body = response.read()
        if response.status == 409:
            raise S3CreateError(response.status, response.reason, body)
        if response.status == 200:
            return Bucket(self, bucket_name)
        else:
            raise S3ResponseError(response.status, response.reason, body)

    def delete_bucket(self, bucket_name, headers=None):
        """
        Removes an S3 bucket.

        In order to remove the bucket, it must first be empty. If the bucket is
        not empty, an ``S3ResponseError`` will be raised.
        """
        response = self.make_request('DELETE', bucket_name, headers=headers)
        body = response.read()
        if response.status != 204:
            raise S3ResponseError(response.status, response.reason, body)

    def generate_url(self, expires_in, method, bucket='', key='', headers=None,
                     query_auth=True, force_http=False, response_headers=None,
                     expires_in_absolute=False, version_id=None):

        headers = headers or {}
        if expires_in_absolute:
            expires = int(expires_in)
        else:
            expires = int(time.time() + expires_in)
        auth_path = self.calling_format.build_auth_path(bucket, key)
        auth_path = self.get_path(auth_path)
        # optional version_id and response_headers need to be added to
        # the query param list.
        extra_qp = []
        query_args = None
        if version_id is not None:
            extra_qp.append("versionId=%s" % version_id)
        if response_headers:
            for k, v in list(response_headers.items()):
                extra_qp.append("%s=%s" % (k, v))
        if extra_qp:
            query_args = '&'.join(extra_qp)

        # if not headers.has_key('Date'):
        #    headers['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

        c_string = auth.canonical_string(method, bucket, key, query_args=query_args, headers=headers, expires=expires)
        b64_hmac = auth.encode(self.access_key_secret, c_string)
        encoded_canonical = parse.quote(b64_hmac, safe='')
        self.calling_format.build_path_base(bucket, key)
        if query_auth:
            encode_ak = self.access_key_id
            # encode_ak = parse.quote(self.access_key_id)
            # print 'encode_ak:%s'%encode_ak
            query_part = '?' + self.QueryString % (encoded_canonical, expires, encode_ak)
        else:
            query_part = ''
        if headers:
            hdr_prefix = self.provider.header_prefix
            for k, v in list(headers.items()):
                if k.startswith(hdr_prefix):
                    # headers used for sig generation must be
                    # included in the url also.
                    extra_qp.append("%s=%s" % (k, parse.quote(v)))
        if extra_qp:
            delimiter = '?' if not query_part else '&'
            query_part += delimiter + '&'.join(extra_qp)
        if force_http:
            protocol = 'http'
            port = 80
        else:
            protocol = self.protocol
            port = self.port
        return self.calling_format.build_url_base(self, protocol,
                                                  self.server_name(port),
                                                  bucket, key) + query_part

    def server_name(self, port=None):
        if not port:
            port = self.port
        if port == 80:
            signature_host = self.host
        else:
            signature_host = "%s:%s" % (self.host, port)
        return signature_host

    def get_path(self, path='/'):
        # The default behavior is to suppress consecutive slashes for reasons
        # discussed at
        # https://groups.google.com/forum/#!topic/boto-dev/-ft0XPUy0y8
        # You can override that behavior with the suppress_consec_slashes param.
        pos = path.find('?')
        if pos >= 0:
            params = path[pos:]
            path = path[:pos]
        else:
            params = None
        if path[-1] == '/':
            need_trailing = True
        else:
            need_trailing = False
        path_elements = self.path.split('/')
        path_elements.extend(path.split('/'))
        path_elements = [p for p in path_elements if p]
        path = '/' + '/'.join(path_elements)
        if path[-1] != '/' and need_trailing:
            path += '/'
        if params:
            path = path + params
        return path

    def get_adp(self, task_id):
        query_args = 'queryadp'
        response = self.make_request('GET', task_id, query_args=query_args)
        body = response.read()
        if response.status != 200:
            raise S3ResponseError(response.status, response.reason, body)
        return body
