from urllib.parse import urlparse


def get_domain(url: str) -> str:
    
    parsed = urlparse(url)

    domain = parsed.netloc

    if domain.startswith("www."):
        domain = domain[4:]

    return domain