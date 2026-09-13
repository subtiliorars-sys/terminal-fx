#!/usr/bin/env python3
"""TermFX Stripe webhook receiver — handles checkout.session.completed events.

Zero external dependencies. Pure Python stdlib.
Run locally: python3 webhook_receiver.py
Deploy to Railway/Fly.io: set STRIPE_WEBHOOK_SECRET env var.

Environment variables:
  STRIPE_WEBHOOK_SECRET — from Stripe Dashboard > Developers > Webhooks
  PORT — HTTP port (default 8080)
"""

import hashlib
import hmac
import json
import os
import time
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# --- Configuration ---
WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
PORT = int(os.environ.get("PORT", "8080"))
SALES_LOG = os.environ.get("SALES_LOG", "sales.json")
DOWNLOAD_BASE = os.environ.get("DOWNLOAD_BASE", "https://github.com/subtiliorars-sys/terminal-fx/releases/latest/download/")
SIGNING_SECRET = os.environ.get("SIGNING_SECRET", "change-me-in-production")

# Map Stripe price IDs -> product files (populated after running setup_stripe.py)
PRICE_TO_PRODUCT = {
    "price_1UF2bn1R997Fg4asAfyBu5PR": {
        "id": "ars",
        "title": "Ars Subtilior — The Subtle Art",
        "file": "termfx-ars.zip",
        "price": 6.99,
    },
    "price_1UF2bo1R997Fg4as8ajFm9PE": {
        "id": "sophia",
        "title": "Sophia — Aeons of Light",
        "file": "termfx-sophia.zip",
        "price": 2.99,
    },
    "price_1UF2bp1R997Fg4asyAHLT3Fq": {
        "id": "maria",
        "title": "Maria — Rosary of Light",
        "file": "termfx-maria.zip",
        "price": 3.99,
    },
    "price_1UF2bp1R997Fg4asB5oYtgeX": {
        "id": "david",
        "title": "David — The Psalmist's Harp",
        "file": "termfx-david.zip",
        "price": 3.99,
    },
    "price_1UF2bq1R997Fg4asucdSwQq0": {
        "id": "light",
        "title": "Light — Light upon Light",
        "file": "termfx-light.zip",
        "price": 2.99,
    },
    "price_1UF2br1R997Fg4asWMzFZReD": {
        "id": "sinai",
        "title": "Sinai — The Parting",
        "file": "termfx-sinai.zip",
        "price": 3.99,
    },
    "price_1UF2bs1R997Fg4asJa1F3xth": {
        "id": "deseret",
        "title": "Deseret — Hive at Dawn",
        "file": "termfx-deseret.zip",
        "price": 2.99,
    },
    "price_1UF2bt1R997Fg4as12RBSzHr": {
        "id": "bundle-sacred",
        "title": "Sacred Collection Bundle",
        "file": "termfx-sacred-collection-bundle.zip",
        "price": 19.99,
    },
}


def verify_signature(payload: bytes, sig_header: str, secret: str) -> bool:
    """Verify Stripe webhook signature using HMAC-SHA256."""
    try:
        timestamp, signatures = "", []
        for item in sig_header.split(","):
            key, _, value = item.partition("=")
            if key == "t":
                timestamp = value
            elif key == "v1":
                signatures.append(value)
    except Exception:
        return False

    if not timestamp or not signatures:
        return False

    # Check timestamp tolerance (5 minutes)
    now = int(time.time())
    if abs(now - int(timestamp)) > 300:
        return False

    signed_payload = f"{timestamp}.{payload.decode('utf-8')}"
    expected = hmac.new(
        secret.encode("utf-8"), signed_payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return any(
        hmac.compare_digest(expected, sig) for sig in signatures
    )


def generate_download_token(product_id: str, customer_email: str, ttl: int = 86400) -> str:
    """Generate a time-limited download token."""
    expires = int(time.time()) + ttl
    payload = f"{product_id}:{customer_email}:{expires}"
    sig = hmac.new(
        SIGNING_SECRET.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()[:16]
    token = base64.urlsafe_b64encode(
        f"{product_id}:{expires}:{sig}".encode("utf-8")
    ).decode("utf-8")
    return token


def log_sale(sale_data: dict) -> None:
    """Append sale to JSON log file."""
    sales = []
    if os.path.exists(SALES_LOG):
        with open(SALES_LOG, "r", encoding="utf-8") as f:
            try:
                sales = json.load(f)
            except json.JSONDecodeError:
                sales = []
    sales.append(sale_data)
    with open(SALES_LOG, "w", encoding="utf-8") as f:
        json.dump(sales, f, indent=2, ensure_ascii=False)
    print(f"  Sale logged: {sale_data.get('product_id')} to {sale_data.get('email')}")


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        sig_header = self.headers.get("Stripe-Signature", "")

        if WEBHOOK_SECRET and not verify_signature(body, sig_header, WEBHOOK_SECRET):
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid signature")
            return

        try:
            event = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return

        event_type = event.get("type", "")

        if event_type == "checkout.session.completed":
            self._handle_checkout_completed(event)
        elif event_type == "payment_intent.succeeded":
            # Can be used for logging
            pass
        else:
            print(f"  Ignoring event type: {event_type}")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def _handle_checkout_completed(self, event: dict) -> None:
        """Process a completed checkout session."""
        session = event.get("data", {}).get("object", {})
        customer_email = session.get("customer_email", "")
        customer_name = session.get("customer_details", {}).get("name", "")
        payment_intent = session.get("payment_intent", "")

        # Get line items
        line_items = session.get("line_items", {}).get("data", [])

        if not line_items:
            # Try expanding line items via payment intent
            print(f"  No line items in session {session.get('id')}, using metadata")
            # Fallback: check session metadata
            product_id = session.get("metadata", {}).get("product_id", "unknown")
            product = PRICE_TO_PRODUCT.get(product_id, {"id": "unknown", "title": "Unknown", "file": "unknown"})
            line_items = [{"price": {"id": product_id}, "quantity": 1}]

        for item in line_items:
            price_id = item.get("price", {}).get("id", "")
            product = PRICE_TO_PRODUCT.get(price_id)
            if not product:
                print(f"  Unknown price ID: {price_id}")
                continue

            # Generate download token
            token = generate_download_token(product["id"], customer_email)
            download_url = f"{DOWNLOAD_BASE}{product['file']}?token={token}"

            sale_record = {
                "timestamp": time.time(),
                "product_id": product["id"],
                "product_title": product["title"],
                "price": product["price"],
                "email": customer_email,
                "name": customer_name,
                "payment_intent": payment_intent,
                "download_token": token,
                "download_url": download_url,
            }

            log_sale(sale_record)

            print(f"  Sale: {product['title']} to {customer_email}")
            print(f"  Download: {download_url}")

    def log_message(self, format, *args):
        """Override to print to stdout instead of stderr."""
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")


def main():
    if not WEBHOOK_SECRET:
        print("WARNING: STRIPE_WEBHOOK_SECRET not set — running in unverified mode")
        print("Set this in production to prevent webhook spoofing.")

    print(f"TermFX webhook receiver starting on port {PORT}...")
    print(f"Sales log: {SALES_LOG}")
    print(f"Download base: {DOWNLOAD_BASE}")

    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
