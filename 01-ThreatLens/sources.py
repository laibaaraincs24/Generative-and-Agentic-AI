import base64
import ipaddress
import re
from datetime import date, datetime
from urllib.parse import urlparse

import requests
import whois


# ============================================================
# INPUT NORMALIZATION
# ============================================================

def normalize_indicator(indicator: str, indicator_type: str) -> str:
    value = indicator.strip()

    if indicator_type == "URL":
        parsed = urlparse(value)
        return parsed.hostname or value

    return value.rstrip(".").lower()


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_indicator(indicator: str, indicator_type: str) -> tuple[bool, str]:
    value = indicator.strip()

    if not value:
        return False, "Please enter an indicator."

    if indicator_type == "IP Address":
        try:
            ipaddress.ip_address(value)
            return True, ""
        except ValueError:
            return False, "Invalid IP address."

    if indicator_type == "Domain":
        domain = value.rstrip(".").lower()

        if len(domain) > 253:
            return False, "Domain name is too long."

        domain_pattern = (
            r"^(?=.{1,253}$)"
            r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
            r"[A-Za-z]{2,63}$"
        )

        if not re.match(domain_pattern, domain):
            return False, "Invalid domain name."

        return True, ""

    if indicator_type == "URL":
        parsed = urlparse(value)

        if parsed.scheme not in ("http", "https"):
            return False, "URL must start with http:// or https://."

        if not parsed.hostname:
            return False, "Invalid URL."

        return True, ""

    return False, "Unknown indicator type."


# ============================================================
# VIRUSTOTAL
# ============================================================

def get_virustotal(
    indicator: str,
    indicator_type: str,
    api_key: str
) -> dict:

    if not api_key:
        return {
            "source": "VirusTotal",
            "status": "error",
            "message": "VirusTotal API key was not provided."
        }

    value = normalize_indicator(indicator, indicator_type)

    headers = {
        "x-apikey": api_key
    }

    try:

        if indicator_type == "IP Address":
            endpoint = (
                "https://www.virustotal.com/api/v3/ip_addresses/"
                + value
            )

        elif indicator_type == "Domain":
            endpoint = (
                "https://www.virustotal.com/api/v3/domains/"
                + value
            )

        elif indicator_type == "URL":
            encoded_url = base64.urlsafe_b64encode(
                value.encode("utf-8")
            ).decode("utf-8").rstrip("=")

            endpoint = (
                "https://www.virustotal.com/api/v3/urls/"
                + encoded_url
            )

        else:
            return {
                "source": "VirusTotal",
                "status": "error",
                "message": "Unsupported indicator type."
            }

        response = requests.get(
            endpoint,
            headers=headers,
            timeout=20
        )

        if response.status_code == 404:
            return {
                "source": "VirusTotal",
                "status": "not_found",
                "message": "Indicator was not found in VirusTotal."
            }

        if response.status_code == 429:
            return {
                "source": "VirusTotal",
                "status": "error",
                "message": "VirusTotal API rate limit reached."
            }

        if response.status_code != 200:
            return {
                "source": "VirusTotal",
                "status": "error",
                "message": (
                    f"VirusTotal returned HTTP "
                    f"{response.status_code}."
                )
            }

        data = response.json()

        attributes = (
            data.get("data", {})
            .get("attributes", {})
        )

        stats = attributes.get(
            "last_analysis_stats",
            {}
        )

        reputation = attributes.get(
            "reputation"
        )

        return {
            "source": "VirusTotal",
            "status": "success",
            "indicator": value,
            "reputation": reputation,
            "analysis_stats": stats,
            "last_analysis_date": attributes.get(
                "last_analysis_date"
            )
        }

    except requests.Timeout:
        return {
            "source": "VirusTotal",
            "status": "error",
            "message": "VirusTotal request timed out."
        }

    except requests.RequestException as exc:
        return {
            "source": "VirusTotal",
            "status": "error",
            "message": f"VirusTotal request failed: {exc}"
        }

    except Exception as exc:
        return {
            "source": "VirusTotal",
            "status": "error",
            "message": f"Unexpected VirusTotal error: {exc}"
        }


# ============================================================
# WHOIS
# ============================================================

def _make_json_safe(value):

    if isinstance(value, (datetime, date)):
        return value.isoformat()

    if isinstance(value, list):
        return [
            _make_json_safe(item)
            for item in value
        ]

    if isinstance(value, dict):
        return {
            str(key): _make_json_safe(item)
            for key, item in value.items()
        }

    return value


def get_whois(
    indicator: str,
    indicator_type: str,
    api_key: str = ""
) -> dict:

   if indicator_type == "IP Address":
    return {
        "source": "WHOIS",
        "status": "not_applicable",
        "message": (
            "Domain WHOIS registration data is not applicable "
            "to IP addresses. Use IP WHOIS/RDAP for network "
            "ownership and registration information."
        )
    }

    hostname = normalize_indicator(
        indicator,
        indicator_type
    )

    try:
        result = whois.whois(hostname)

        if not result:
            return {
                "source": "WHOIS",
                "status": "not_found",
                "message": "No WHOIS information was returned."
            }

        result_dict = dict(result)

        safe_result = _make_json_safe(
            result_dict
        )

        return {
            "source": "WHOIS",
            "status": "success",
            "domain": hostname,
            "data": safe_result
        }

    except Exception as exc:
        return {
            "source": "WHOIS",
            "status": "error",
            "message": f"WHOIS lookup failed: {exc}"
        }


# ============================================================
# SOURCE REGISTRY
# ============================================================

SOURCES = {
    "VirusTotal": get_virustotal,
    "WHOIS": get_whois,
}
