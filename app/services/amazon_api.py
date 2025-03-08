# app/services/amazon_api.py
import httpx
import hmac
import hashlib
import datetime
import urllib.parse
from typing import List, Dict
from app.config import settings


class AmazonAPIError(Exception):
    pass


class AmazonAPI:
    def __init__(self):
        self.service = "ProductAdvertisingAPI"
        self.target = "com.amazon.paapi5.v1.SearchItems"

    async def search_products(self, keywords: str, max_price: float) -> List[Dict]:
        """Search Amazon products with proper authentication"""
        try:
            headers = self._generate_headers()
            payload = self._create_payload(keywords, max_price)

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{settings.amazon_host}/paapi5/searchitems",
                    headers=headers,
                    json=payload,
                    timeout=10,
                )
                response.raise_for_status()
                return self._parse_response(response.json())

        except Exception as e:
            raise AmazonAPIError(f"Amazon API error: {str(e)}")

    def _create_payload(self, keywords: str, max_price: float) -> Dict:
        return {
            "Keywords": keywords,
            "PartnerTag": settings.amazon_associate_tag,
            "PartnerType": "Associates",
            "Marketplace": "www.amazon.com",
            "Resources": [
                "ItemInfo.Title",
                "Offers.Listings.Price",
                "Images.Primary.Medium",
            ],
            "MaxPrice": max_price * 100 if max_price else None,
            "ItemCount": 5,
        }

    def _generate_headers(self) -> Dict:
        """Generate AWS Signature v4 headers"""
        now = datetime.datetime.utcnow()
        amz_date = now.strftime("%Y%m%dT%H%M%SZ")
        date_stamp = now.strftime("%Y%m%d")

        # Signature calculation
        canonical_request = self._create_canonical_request(amz_date)
        string_to_sign = self._create_string_to_sign(
            canonical_request, date_stamp, amz_date
        )
        signature = self._calculate_signature(string_to_sign, date_stamp)

        return {
            "Content-Encoding": "amz-1.0",
            "Content-Type": "application/json",
            "X-Amz-Date": amz_date,
            "X-Amz-Target": self.target,
            "Authorization": self._create_auth_header(signature, date_stamp, amz_date),
        }

    def _create_canonical_request(self, amz_date: str) -> str:
        return "\n".join(
            [
                "POST",
                "/paapi5/searchitems",
                "",
                f"host:{settings.amazon_host}",
                f"x-amz-date:{amz_date}",
                "",
                "host;x-amz-date",
                hashlib.sha256(b"").hexdigest(),
            ]
        )

    def _create_string_to_sign(
        self, canonical_request: str, date_stamp: str, amz_date: str
    ) -> str:
        return "\n".join(
            [
                "AWS4-HMAC-SHA256",
                amz_date,
                f"{date_stamp}/{settings.amazon_region}/{self.service}/aws4_request",
                hashlib.sha256(canonical_request.encode()).hexdigest(),
            ]
        )

    def _calculate_signature(self, string_to_sign: str, date_stamp: str) -> str:
        def sign(key, msg):
            return hmac.new(key, msg.encode(), hashlib.sha256).digest()

        k_date = sign(f"AWS4{settings.amazon_secret_key}".encode(), date_stamp)
        k_region = sign(k_date, settings.amazon_region)
        k_service = sign(k_region, self.service)
        k_signing = sign(k_service, "aws4_request")
        return hmac.new(k_signing, string_to_sign.encode(), hashlib.sha256).hexdigest()

    def _create_auth_header(
        self, signature: str, date_stamp: str, amz_date: str
    ) -> str:
        return (
            f"AWS4-HMAC-SHA256 Credential={settings.amazon_access_key}/"
            f"{date_stamp}/{settings.amazon_region}/{self.service}/aws4_request, "
            f"SignedHeaders=host;x-amz-date, Signature={signature}"
        )

    def _parse_response(self, response: Dict) -> List[Dict]:
        """Parse Amazon API response into our format"""
        results = []
        for item in response.get("SearchResult", {}).get("Items", []):
            try:
                results.append(
                    {
                        "name": item["ItemInfo"]["Title"]["DisplayValue"],
                        "price": float(
                            item["Offers"]["Listings"][0]["Price"][
                                "DisplayAmount"
                            ].replace("$", "")
                        ),
                        "category": item.get("BrowseNodeInfo", {})
                        .get("BrowseNodes", [{}])[0]
                        .get("Name", "General"),
                        "url": item["DetailPageURL"],
                        "image": item["Images"]["Primary"]["Medium"]["URL"],
                    }
                )
            except (KeyError, IndexError):
                continue
        return results
