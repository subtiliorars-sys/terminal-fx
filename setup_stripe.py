#!/usr/bin/env python3
"""Stripe product and payment link generator for TermFX.

Zero external dependencies — uses Python standard library urllib.
Reads products/manifest.json and creates:
1. Stripe Products
2. Stripe Prices (one-time)
3. Stripe Payment Links (hosted checkout URLs: https://buy.stripe.com/...)

Saves output to products/stripe_links.json and updates landing/index.html.

Usage:
    export STRIPE_SECRET_KEY="sk_live_..."
    python3 setup_stripe.py --dry-run
    python3 setup_stripe.py
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = BASE_DIR / "products" / "manifest.json"
OUTPUT_PATH = BASE_DIR / "products" / "stripe_links.json"
LANDING_HTML_PATH = BASE_DIR / "landing" / "index.html"

BUNDLE_PRODUCT = {
    "id": "bundle-sacred",
    "title": "TermFX: Sacred Collection Complete Bundle",
    "theme": "Complete Sacred Collection",
    "blurb": "All 7 sacred visual meditations + Ars Subtilior music generator + bonus motet WAV audio + starfield.",
    "price": 19.99,
}

def stripe_api_request(endpoint: str, api_key: str, data: dict = None) -> dict:
    url = f"https://api.stripe.com/v1/{endpoint}"
    encoded_data = urllib.parse.urlencode(data).encode("utf-8") if data else None
    
    req = urllib.request.Request(
        url,
        data=encoded_data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/x-www-form-urlencoded",
        }
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
            msg = err_json.get("error", {}).get("message", err_body)
        except Exception:
            msg = err_body
        raise RuntimeError(f"Stripe API Error ({e.code} on {endpoint}): {msg}")

def main():
    parser = argparse.ArgumentParser(description="Create Stripe products & payment links for TermFX.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without creating Stripe objects")
    parser.add_argument("--key", type=str, default=None, help="Stripe secret key (defaults to STRIPE_SECRET_KEY env var)")
    args = parser.parse_args()

    api_key = args.key or os.environ.get("STRIPE_SECRET_KEY")

    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    items = [item for item in manifest.get("items", []) if not item.get("free") and not item.get("upload_as_extra")]
    items.append(BUNDLE_PRODUCT)

    print(f"Loaded {len(items)} paid products to configure with Stripe.")

    if not api_key:
        if args.dry_run:
            print("[DRY RUN] No STRIPE_SECRET_KEY provided, proceeding with simulated output...")
            api_key = "sk_test_simulated"
        else:
            print("ERROR: STRIPE_SECRET_KEY environment variable not set.")
            print("Usage: STRIPE_SECRET_KEY=sk_live_... python3 setup_stripe.py")
            print("Or pass --dry-run to preview what will be created.")
            sys.exit(1)

    results = {}

    for item in items:
        prod_id = item["id"]
        title = item["title"]
        blurb = item.get("blurb", "")
        price_usd = item["price"]
        amount_cents = int(round(price_usd * 100))

        print(f"\nProcessing '{prod_id}': {title} (${price_usd:.2f})")

        if args.dry_run:
            fake_prod = f"prod_sim_{prod_id}"
            fake_price = f"price_sim_{prod_id}"
            fake_link = f"https://buy.stripe.com/sim_{prod_id}"
            print(f"  [DRY RUN] Would create product: '{title}'")
            print(f"  [DRY RUN] Would create price: {amount_cents} cents USD")
            print(f"  [DRY RUN] Would create payment link -> {fake_link}")
            results[prod_id] = {
                "title": title,
                "price_usd": price_usd,
                "product_id": fake_prod,
                "price_id": fake_price,
                "payment_url": fake_link,
            }
            continue

        # 1. Create Product
        print(f"  Creating Stripe Product...")
        prod_res = stripe_api_request("products", api_key, {
            "name": title,
            "description": blurb[:500],
            "metadata[project]": "termfx",
            "metadata[item_id]": prod_id,
        })
        stripe_prod_id = prod_res["id"]
        print(f"    Product ID: {stripe_prod_id}")

        # 2. Create Price
        print(f"  Creating Stripe Price...")
        price_res = stripe_api_request("prices", api_key, {
            "product": stripe_prod_id,
            "unit_amount": amount_cents,
            "currency": "usd",
            "metadata[project]": "termfx",
            "metadata[item_id]": prod_id,
        })
        stripe_price_id = price_res["id"]
        print(f"    Price ID: {stripe_price_id}")

        # 3. Create Payment Link
        print(f"  Creating Stripe Payment Link...")
        link_res = stripe_api_request("payment_links", api_key, {
            "line_items[0][price]": stripe_price_id,
            "line_items[0][quantity]": 1,
            "metadata[project]": "termfx",
            "metadata[item_id]": prod_id,
        })
        payment_url = link_res["url"]
        print(f"    Payment URL: {payment_url}")

        results[prod_id] = {
            "title": title,
            "price_usd": price_usd,
            "product_id": stripe_prod_id,
            "price_id": stripe_price_id,
            "payment_url": payment_url,
        }

    OUTPUT_PATH.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nWrote results to {OUTPUT_PATH}")

    # Update landing page if it exists
    if LANDING_HTML_PATH.exists() and not args.dry_run:
        html = LANDING_HTML_PATH.read_text(encoding="utf-8")
        updated = False
        for prod_id, info in results.items():
            placeholder = f"{{{{STRIPE_URL_{prod_id.upper().replace('-', '_')}}}}}"
            if placeholder in html:
                html = html.replace(placeholder, info["payment_url"])
                updated = True
        if updated:
            LANDING_HTML_PATH.write_text(html, encoding="utf-8")
            print(f"Updated Stripe links inside {LANDING_HTML_PATH}")

    print("Finished successfully!")

if __name__ == "__main__":
    main()
