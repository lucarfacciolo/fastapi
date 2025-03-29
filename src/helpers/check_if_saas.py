from datetime import datetime

# (NOTE lfacciolo) found this keywords that points to a saas company
saas_keywords = [
    "subscription",
    "cloud",
    "cloud-based",
    "per-user",
    "monthly pricing",
    "annual subscription",
    "usage-based",
    "SaaS",
    "software as a service",
    "pay-as-you-go",
    "recurring",
    "tiered pricing",
    "license-based",
    "web portal",
    "API access",
    "hosted solution",
    "on-demand",
    "scalable",
    "multi-tenant",
    "self-service",
    "platform as a service",
    "PaaS",
    "per-seat",
    "pay per use",
    "metered billing",
    "subscription model",
    "cloud-hosted",
    "web-based",
    "remote access",
    "centralized management",
]


def is_saas(description: str) -> bool:
    description_lower = description.lower()
    return any(keyword in description_lower for keyword in saas_keywords)
