import re
from urllib.parse import urlparse

def extract_features(url):
    parsed = urlparse(url)
    domain = parsed.netloc

    return {
        "having_IPhaving_IP_Address": 1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else -1,
        "URLURL_Length": 1 if len(url) < 54 else -1,
        "Shortining_Service": -1 if re.search(r'bit\.ly|goo\.gl|tinyurl', url) else 1,
        "having_At_Symbol": -1 if '@' in url else 1,
        "double_slash_redirecting": -1 if url.rfind('//') > 6 else 1,
        "Prefix_Suffix": -1 if '-' in domain else 1,
        "having_Sub_Domain": -1 if domain.count('.') > 2 else 1
    }
