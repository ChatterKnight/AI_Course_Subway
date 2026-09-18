

# API key for FLUX 2 [pro] from Black Forest Labs
# bfl_k73X3K7X5PwX1gVPyUiv3rhWzMnkgm60


prompt_text = 'An image of a tuna-ketchup footlong subway sandwich, being deliciously eaten in someones mouth. Keep in mind its being EATEN and is a footlong sandwich'

# ----------------------------------------------------------------

import requests
import os
import time

API_KEY = "bfl_k73X3K7X5PwX1gVPyUiv3rhWzMnkgm60"


def as_json(response):
    # An error page (HTML 502, proxy timeout) is not JSON. Report it instead of
    # raising a bare JSONDecodeError.
    try:
        return response.json()
    except ValueError:
        raise SystemExit(f"Stopped: {response.status_code} {response.text[:200]}")


# Submit generation request
response = as_json(requests.post(
    "https://api.bfl.ai/v1/flux-2-pro",
    headers={
        "accept": "application/json",
        "x-key": API_KEY,
        "Content-Type": "application/json",
    },
    json={
        "prompt": prompt_text,
        "width": 1920,
        "height": 1080
    },
))

print(f'Generating:"{prompt_text}"...')

# ----------------------------------------------------------------

polling_url = response.get("polling_url")
if not polling_url:
    raise SystemExit(f"Submit failed: {response}")

# Poll for result
while True:
    result = as_json(requests.get(
        polling_url,
        headers={
            "accept": "application/json",
            "x-key": API_KEY
        }
    ))

    status = result.get("status")

    if status != "Pending":
        if status == "Ready":
            print(f"Image URL: {result['result']['sample']}")
            break
        raise SystemExit(f"Stopped: {status}")

    time.sleep(0.5)