import re
import json

# ----------------------------------------
# Step 1: Read the receipt text file
# ----------------------------------------
with open("/Users/zainitdinspv/work/practice5/raw.txt", "r", encoding="utf-8") as file:
    text = file.read()


# ----------------------------------------
# Step 2: Extract product names
# ----------------------------------------
product_pattern = r"\d+\.\n(.+)"
products = re.findall(product_pattern, text)
products = [p.strip() for p in products]


# ----------------------------------------
# Step 3: Extract UNIT prices (price for 1 item)
# ----------------------------------------
unit_price_pattern = r"x\s*([\d\s]+,\d{2})"
unit_prices = re.findall(unit_price_pattern, text)

# Convert to float
def clean_price(price):
    return float(price.replace(" ", "").replace(",", "."))

unit_prices = [clean_price(p) for p in unit_prices]


# ----------------------------------------
# Step 4: Calculate total from unit prices
# ----------------------------------------
calculated_total = sum(unit_prices)


# ----------------------------------------
# Step 5: Extract date and time
# ----------------------------------------
datetime_pattern = r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}"
datetime_match = re.search(datetime_pattern, text)
datetime = datetime_match.group() if datetime_match else None


# ----------------------------------------
# Step 6: Extract payment method
# ----------------------------------------
payment_pattern = r"(Банковская карта|Наличные)"
payment_match = re.search(payment_pattern, text)
payment_method = payment_match.group() if payment_match else None


# ----------------------------------------
# Step 7: Extract official total
# ----------------------------------------
official_total_pattern = r"ИТОГО:\n([\d\s]+,\d{2})"
official_total_match = re.search(official_total_pattern, text)
official_total = clean_price(official_total_match.group(1)) if official_total_match else None


# ----------------------------------------
# Step 8: Create structured output
# ----------------------------------------
data = {
    "products": products,
    "unit_prices": unit_prices,
    "calculated_total": calculated_total,
    "official_total": official_total,
    "payment_method": payment_method,
    "datetime": datetime
}


# ----------------------------------------
# Step 9: Output results
# ----------------------------------------
print(json.dumps(data, indent=4, ensure_ascii=False))