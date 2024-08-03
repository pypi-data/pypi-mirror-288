# Carbon Webhooks Python Library

`carbon_webhooks_python` is a Python library designed to verify Carbon webhook events. This library provides a simple way to validate webhook signatures and ensure the authenticity of incoming requests.

## Features

- **Generate Signature**: Generate HMAC SHA256 signatures for webhook payloads.
- **Validate Signature**: Validate incoming webhook signatures to ensure they match the expected signature.
- **Extract Signature Header**: Parse and extract components from the Carbon-Signature header.

## Installation

You can install the library using pip:

```bash
pip install carbon-verifier
```

### `WebhookVerifier`

#### `__init__(signing_key: str)`

*   `signing_key`: Your Carbon webhook signing key.

#### `generate_signature(timestamp: str, json_payload: str) -> str`

Generates a signature for the given timestamp and JSON payload.

*   `timestamp`: The timestamp of the webhook event.
*   `json_payload`: The JSON payload of the webhook event.

Returns the generated signature.

#### `validate_signature(received_sig: str, timestamp: str, payload: str) -> bool`

Validates the received signature against the generated signature.

*   `received_sig`: The received signature to validate.
*   `timestamp`: The timestamp of the webhook event.
*   `payload`: The JSON payload of the webhook event.

Returns `true` if the signature is valid, otherwise `false`.

#### `extract_signature_header(header: str) -> Any`

Extracts the timestamp and signature from the Carbon-Signature header.

*   `header`: The Carbon-Signature header.

Returns an object with the extracted signature parts.

## Example Usage

Here is an example demonstrating how to use the `carbon_verifier` library to verify a Carbon webhook:

```python
from carbon_verifier import WebhookVerifier
import json

# Initialize the verifier with your signing key
SIGNING_SECRET = 'aa76aee859f223451fd9bfb37ce893a0'  # Replace with your actual signing key
verifier = WebhookVerifier(SIGNING_SECRET)

def verify_webhook(headers, payload):
    carbon_signature = headers.get('Carbon-Signature')
    if not carbon_signature:
        return {'status': 'error', 'message': 'Missing Carbon-Signature header'}, 400

    try:
        timestamp, received_signature = WebhookVerifier.extract_signature_header(carbon_signature)
    except ValueError:
        return {'status': 'error', 'message': 'Invalid Carbon-Signature header format'}, 400

    if not verifier.validate_signature(received_signature, timestamp, payload):
        return {'status': 'error', 'message': 'Invalid signature'}, 400

    data = json.loads(payload)
    print("Received webhook data:", data)

    # Handle the event
    event_type = data.get('webhook_type')
    if event_type == 'example_event':
        # Process the event
        print("Processing example_event")

    return {'status': 'success'}, 200

# Hardcoded payload for example
payload_v1 = '{"payload": "{\\"webhook_type\\": \\"FILES_CREATED\\", \\"obj\\": {\\"object_type\\": \\"FILE_LIST\\", \\"object_id\\": [\\"46654\\"], \\"additional_information\\": \\"null\\"}, \\"customer_id\\": \\"satvik\\", \\"timestamp\\": \\"1721392406\\"}"}'

# Hardcoded header for example
headers = {
  "Content-Type": "application/json",
  "Carbon-Signature": "t=1721392406,v1=aa2273ab64bb9162e7e7983a9cd7ab9f90d686691b1fd25c577991ad42c53fc1",
  "Carbon-Signature-Compact": "t=1721392406,v2=42a86d4083fee090b5a0800a91e82fb389f0bed4da757d07ee8ba97485194e59"
}

result, status_code = verify_webhook(headers, payload_v1)
print(f"Verification Result: {result}, Status Code: {status_code}")
