import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else -1)     # 1
    features.append(1 if len(url) < 54 else -1)                            # 2
    features.append(-1 if re.search(r'bit\.ly|goo\.gl|tinyurl', url) else 1)  # 3
    features.append(-1 if '@' in url else 1)                               # 4
    features.append(-1 if url.rfind('//') > 6 else 1)                      # 5
    features.append(-1 if '-' in urlparse(url).netloc else 1)              # 6
    features.append(-1 if urlparse(url).netloc.count('.') > 2 else 1)      # 7

    # Fill remaining features to EXACTLY 31
    while len(features) < 31:
        features.append(1)

    print("DEBUG: Feature length =", len(features))  # 👈 VERY IMPORTANT

    return features
