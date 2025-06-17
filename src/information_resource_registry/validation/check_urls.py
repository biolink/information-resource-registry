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


def is_valid_url(url: str) -> bool:
    try:
        # Add a randomized sleep to avoid rapid requests
        time.sleep(random.uniform(1, 3))
        response = http.request("GET", url, headers={'User-Agent': 'Mozilla/5.0'})

        # Check if the response status is 200 for a valid URL
        if response.status == 403:
            return True
        return response.status == 200

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
