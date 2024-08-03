# Carbon Webhooks Python Library

`carbon_webhooks_python` is a Python library designed to verify Carbon webhook events. This library provides a simple way to validate webhook signatures and ensure the authenticity of incoming requests.

## Features

- **Generate Signature**: Generate HMAC SHA256 signatures for webhook payloads.
- **Validate Signature**: Validate incoming webhook signatures to ensure they match the expected signature.
- **Extract Signature Header**: Parse and extract components from the Carbon-Signature header.

## Installation

You can install the library using pip:

```bash
pip install carbon_webhooks
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