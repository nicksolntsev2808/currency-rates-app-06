API_BASE = "https://api.frankfurter.app/latest"
TARGETS = ("EUR", "GBP", "PLN", "CZK")


def is_valid_code(code):
    return len(code) == 3 and code.isalpha()


def build_url(base):
    targets = ",".join(t for t in TARGETS if t != base)
    return f"{API_BASE}?from={base}&to={targets}"


def format_rates(base, payload):
    return {
        "base": base,
        "date": payload.get("date"),
        "rates": {code: round(value, 4) for code, value in payload.get("rates", {}).items()},
    }
