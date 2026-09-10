import os
import time
import random
from pathlib import Path
from tqdm import tqdm
import yaml
import urllib3
from urllib3.util.ssl_ import create_urllib3_context
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed

# Path to the YAML file containing URLs
INFORES_YAML = os.path.join('infores_catalog.yaml')

# SSL context for handling legacy server connections
ctx = create_urllib3_context()
ctx.load_default_certs()
ctx.options |= 0x4  # ssl.OP_LEGACY_SERVER_CONNECT

# Define retry strategy
retry_strategy = Retry(
    total=3,  # Reduce the number of retries to avoid hammering sites
    backoff_factor=1,  # Backoff factor for retries
    status_forcelist=[500, 502, 503, 504],  # Retry on these status codes
)

# Use a global http PoolManager for reuse across requests
http = urllib3.PoolManager(ssl_context=ctx,
                           retries=retry_strategy,
                           timeout=urllib3.util.Timeout(connect=10, read=30))


# Browser-like headers. A bare "Mozilla/5.0" is rejected by many CDNs/WAFs
# (Cloudflare, Akamai), producing false "invalid" results for live sites.
BROWSER_HEADERS = {
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/124.0.0.0 Safari/537.36'),
    'Accept': ('text/html,application/xhtml+xml,application/xml;q=0.9,'
               'image/avif,image/webp,*/*;q=0.8'),
    'Accept-Language': 'en-US,en;q=0.9',
}

# CURIE prefixes that are xrefs but not web URLs. Expand the ones we know how
# to resolve; anything else non-HTTP is an identifier, not a URL to fetch.
CURIE_URL_PREFIXES = {
    'fairsharing': 'https://fairsharing.org/',
}

# Non-2xx/3xx statuses that still mean "the server answered and the resource is
# really there", even though a bot didn't get a success: auth walls, rate
# limits, or servers that reject GET method probing.
REACHABLE_STATUSES = {401, 403, 405, 429}


def status_ok(status: int) -> bool:
    # Any 2xx (e.g. PubMed answers 203 Non-Authoritative) or 3xx redirect
    # (often a WAF challenge with no Location, or http->https) means the link
    # resolves. urllib3 auto-follows redirects that carry a Location, so a bare
    # 3xx here is a link that resolves but the client couldn't chase. 5xx are
    # left as failures on purpose: the resource is not being served.
    return 200 <= status < 400 or status in REACHABLE_STATUSES


def normalize_xref(xref: str) -> str | None:
    """Return an HTTP(S) URL to validate, or None if the xref is a bare
    identifier/CURIE that should not be fetched as a URL."""
    if xref.startswith(('http://', 'https://')):
        return xref
    scheme, _, rest = xref.partition(':')
    if scheme in CURIE_URL_PREFIXES and rest:
        return CURIE_URL_PREFIXES[scheme] + rest
    # Unknown CURIE / bare identifier: not a URL, nothing to validate.
    return None


def is_valid_url(url: str) -> bool:
    # A CURIE or bare identifier is not a fetchable URL; don't flag it.
    resolved = normalize_xref(url)
    if resolved is None:
        return True
    url = resolved
    try:
        # Add a randomized sleep to avoid rapid requests
        time.sleep(random.uniform(1, 3))
        response = http.request("GET", url, headers=BROWSER_HEADERS)

        # Treat any status that proves the resource exists as valid.
        return status_ok(response.status)

    except urllib3.exceptions.MaxRetryError:
        print(f"Max retries exceeded for URL: {url} - invalid")
        return False

    except urllib3.exceptions.TimeoutError:
        print(f"Timeout error for URL: {url} - invalid")
        return False

    except urllib3.exceptions.SSLError as e:
        print(f"SSL error for URL {url}: {e} - invalid")
        return False

    except urllib3.exceptions.HTTPError as e:
        print(f"HTTP error for URL {url}: {e} - invalid")
        return False

    except urllib3.exceptions.RequestError as e:
        print(f"General request error for URL {url}: {e} - invalid")
        return False


def load_urls_from_yaml() -> list:
    """Load URLs from a YAML file."""
    infores_catalog = Path(__file__).parents[3] / 'infores_catalog.yaml'
    try:
        with open(infores_catalog, 'r') as file:
            data = yaml.safe_load(file)
            return data.get('information_resources', [])
    except FileNotFoundError:
        print(f"File not found: {infores_catalog}")
        return []


def main():
    """Main function to validate URLs."""
    # Load URLs from the YAML file
    data = load_urls_from_yaml()
    invalid_resource_urls = []

    # Count the total number of xrefs to process for the status bar
    total_xrefs = sum(len(infores.get('xref', [])) for infores in data)

    # Initialize tqdm progress bar with the total number of URLs
    with tqdm(total=total_xrefs, desc="Validating URLs", unit="url") as pbar:
        # Use ThreadPoolExecutor to parallelize URL validation
        with ThreadPoolExecutor() as executor:
            future_to_infores = {}

            # Submit each URL check as a task
            for infores in data:
                if 'xref' not in infores.keys():
                    if infores.get('status') != 'deprecated':
                        print(f"Information resource {infores.get('id')} does not have a URL.")
                else:
                    for xref in infores.get('xref'):
                        if infores.get('status') != 'deprecated':
                            # Submit the is_valid_url task to the executor
                            future = executor.submit(is_valid_url, xref)
                            future_to_infores[future] = (infores.get('id'), xref)

            # Process completed futures as they finish
            for future in as_completed(future_to_infores):
                infores_id, xref = future_to_infores[future]
                is_valid = future.result()

                if not is_valid:
                    print(f"URL: {xref} - invalid")
                    invalid_resource_urls.append((infores_id, xref))

                # Update the progress bar
                pbar.update(1)

    # if invalid_resource_urls:
    #     raise ValueError(f"Invalid URLs found: {invalid_resource_urls}")

if __name__ == "__main__":
    main()
