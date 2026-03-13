"""
Canonical whitelist of allowed spending category and merchant names.
The LLM and API endpoints must only use names from these sets.
New names can only be added here explicitly — not dynamically by the LLM.
"""

ALLOWED_CATEGORIES: frozenset = frozenset({
    "online shopping",      # All online purchases
    "offline spends",       # All in-store / POS purchases
    "fuel",                 # Petrol, diesel, CNG (includes surcharge waiver)
    "dining",               # Restaurants, cafes, QSR
    "food delivery",        # Swiggy, Zomato, BigBasket orders
    "grocery",              # Supermarkets, grocery stores
    "travel",               # Flights, hotels, cabs, train
    "utilities",            # Electricity, gas, internet, DTH, phone bills
    "rent",                 # Rental payments
    "insurance",            # Insurance premiums
    "education",            # School / college fees, ed-tech
    "government payments",  # Taxes, govt portals
    "international",        # Forex / overseas transactions
    "entertainment",        # Movies, OTT, gaming, fitness
    "wallets",              # Digital wallet top-ups, UPI
})

ALLOWED_MERCHANTS: frozenset = frozenset({
    "amazon",       # E-commerce
    "flipkart",     # E-commerce
    "swiggy",       # Food delivery
    "zomato",       # Food delivery
    "bigbasket",    # Grocery delivery
    "blinkit",      # Quick commerce
    "myntra",       # Fashion
    "uber",         # Mobility
    "ola",          # Mobility
    "bookmyshow",   # Entertainment / ticketing
    "phonepe",      # Payments
    "airtel",       # Telecom
    "netflix",      # OTT
    "nykaa",        # Beauty
    "ajio",         # Fashion
})


# Ordered lists for consistent display in comparison report
ORDERED_CATEGORIES: list = [
    "online shopping",
    "offline spends",
    "dining",
    "food delivery",
    "grocery",
    "fuel",
    "travel",
    "entertainment",
    "utilities",
    "wallets",
    "rent",
    "insurance",
    "education",
    "government payments",
    "international",
]

ORDERED_MERCHANTS: list = [
    "amazon",
    "flipkart",
    "swiggy",
    "zomato",
    "bigbasket",
    "blinkit",
    "myntra",
    "uber",
    "ola",
    "bookmyshow",
    "phonepe",
    "airtel",
    "netflix",
    "nykaa",
    "ajio",
]


def validate_category_name(name: str) -> str:
    """
    Normalize and validate a category name against the whitelist.
    Returns the normalized name if valid.
    Raises ValueError if not in the allowed list.
    """
    normalized = name.lower().strip()
    if normalized not in ALLOWED_CATEGORIES:
        raise ValueError(
            f"Category '{name}' is not in the allowed list. "
            f"Use one of the {len(ALLOWED_CATEGORIES)} canonical category names."
        )
    return normalized


def validate_merchant_name(name: str) -> str:
    """
    Normalize and validate a merchant name against the whitelist.
    Returns the normalized name if valid.
    Raises ValueError if not in the allowed list.
    """
    normalized = name.lower().strip()
    if normalized not in ALLOWED_MERCHANTS:
        raise ValueError(
            f"Merchant '{name}' is not in the allowed list. "
            f"Use one of the {len(ALLOWED_MERCHANTS)} canonical merchant names."
        )
    return normalized
