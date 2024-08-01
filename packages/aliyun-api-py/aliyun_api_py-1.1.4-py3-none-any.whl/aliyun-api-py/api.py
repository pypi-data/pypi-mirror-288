import hashlib
import hmac
from collections import OrderedDict
from urllib.parse import urlencode, quote_plus
import pytz
import requests
from datetime import datetime
import uuid


def percent_code(encoded_str):
    return encoded_str.replace("+", "%20").replace("*", "%2A").replace("%7E", "~")


class Api:
    def __init__(self, access_key_id, access_key_secret, http_method, host, uri, x_acs_action, x_acs_version,
                 algorithm="ACS3-HMAC-SHA256"):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.http_method = http_method
        self.host = host
        self.canonical_uri = uri
        self.algorithm = algorithm
        self.headers = OrderedDict()
        self.param = OrderedDict()
        self.body = None

        # 初始化headers
        self.headers["host"] = self.host
        self.headers["x-acs-action"] = x_acs_action
        self.headers["x-acs-version"] = x_acs_version
        self.headers["x-acs-date"] = datetime.now(pytz.timezone("Etc/GMT")).strftime("%Y-%m-%dT%H:%M:%SZ")
        self.headers["x-acs-signature-nonce"] = str(uuid.uuid4())

    def exec(self):
        # 对查询参数按名称排序并返回编码后的字符串
        self.param = {k: v for k, v in sorted(self.param.items(), key=lambda item: item[0])}

        # 构造认证信息
        try:
            canonical_query_string = "&".join(
                f"{percent_code(quote_plus(k))}={percent_code(quote_plus(str(v)))}" for k, v in
                self.param.items())
            hashed_request_payload = hashlib.sha256((self.body or "").encode("utf-8")).hexdigest()
            self.headers["x-acs-content-sha256"] = hashed_request_payload
            self.headers = {k: v for k, v in sorted(self.headers.items(), key=lambda item: item[0])}

            signed_headers = ";".join(sorted(self.headers.keys(), key=lambda x: x.lower()))
            canonical_request = (f"{self.http_method}\n{self.canonical_uri}\n{canonical_query_string}\n"
                                 f"{"\n".join(f"{k.lower()}:{v}" for k, v in self.headers.items() if
                                              k.lower().startswith("x-acs-") or k.lower() in ["host", "content-type"])}"
                                 f"\n\n{signed_headers}\n{hashed_request_payload}")
            string_to_sign = f"{self.algorithm}\n{hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()}"
            signature = (hmac.new(self.access_key_secret.encode("utf-8"), string_to_sign.encode("utf-8"),
                                  hashlib.sha256).digest().hex().lower())

            self.headers["Authorization"] = (f"{self.algorithm} Credential={self.access_key_id},"
                                             f"SignedHeaders={signed_headers},Signature={signature}")
        except Exception as e:
            return e

        # 发起请求
        url = f"https://{self.host}{self.canonical_uri}"
        if self.param:
            url += "?" + urlencode(self.param, doseq=True, safe='*')

        try:
            response = requests.request(method=self.http_method, url=url,
                                        headers={k: v for k, v in self.headers.items()}, data=self.body)
            response.raise_for_status()
            return {"status_code": response.status_code,
                    "headers": response.headers,
                    "body": response.text
                    }
        except requests.RequestException as e:
            return e
