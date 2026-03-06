import re
import json

# ----------------------------------------
# Step 1: Read the receipt text file
# ----------------------------------------
# The raw receipt is stored in raw.txt.
# We open the file using UTF-8 encoding because the text contains Cyrillic characters.
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()


# ----------------------------------------
# Step 2: Extract all price values
# ----------------------------------------
# Regex explanation:
# \d          -> a digit
# [\d\s]*     -> any number of digits or spaces (to handle prices like "1 200")
# ,\d{2}      -> comma followed by exactly 2 digits (decimal part)
# Example matches:
# 154,00
# 1 200,00
price_pattern = r"\d[\d\s]*,\d{2}"

# re.findall returns ALL matches of the pattern in the text
prices = re.findall(price_pattern, text)


# ----------------------------------------
# Step 3: Extract product names
# ----------------------------------------
# In the receipt, each product starts with a number like:
# 1.
# Product name
#
# Regex explanation:
# \d+\.   -> product number (1., 2., 3. etc.)
# \n      -> new line
# (.+)    -> capture the product name
product_pattern = r"\d+\.\n(.+)"

products = re.findall(product_pattern, text)

# Remove extra spaces from product names
products = [p.strip() for p in products]


# ----------------------------------------
# Step 4: Extract item totals
# ----------------------------------------
# After each product there is a line with the final price:
# Example:
# 308,00
# Стоимость
#
# Regex explanation:
# \n([\d\s]+,\d{2}) -> capture the price on a separate line
# \nСтоимость       -> confirm it is followed by the word "Стоимость"
item_total_pattern = r"\n([\d\s]+,\d{2})\nСтоимость"

item_totals = re.findall(item_total_pattern, text)


# ----------------------------------------
# Step 5: Convert prices from text to numbers
# ----------------------------------------
# Prices in the receipt use:
# - spaces for thousands ("1 200")
# - comma for decimals ("154,00")
#
# Python requires:
# - no spaces
# - decimal point instead of comma
def clean_price(price):
    return float(price.replace(" ", "").replace(",", "."))


# Apply conversion to all extracted totals
item_totals = [clean_price(p) for p in item_totals]


# ----------------------------------------
# Step 6: Calculate the total amount
# ----------------------------------------
# We sum all individual product totals
calculated_total = sum(item_totals)


# ----------------------------------------
# Step 7: Extract date and time
# ----------------------------------------
# Regex explanation:
# \d{2}\.\d{2}\.\d{4} -> date format (dd.mm.yyyy)
# \s                  -> space
# \d{2}:\d{2}:\d{2}   -> time format (hh:mm:ss)
datetime_pattern = r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}"

datetime_match = re.search(datetime_pattern, text)

# If match found, extract the value
datetime = datetime_match.group() if datetime_match else None


# ----------------------------------------
# Step 8: Extract payment method
# ----------------------------------------
# The receipt may contain payment methods such as:
# "Банковская карта" (bank card)
# or "Наличные" (cash)
payment_pattern = r"(Банковская карта|Наличные)"

payment_match = re.search(payment_pattern, text)

payment_method = payment_match.group() if payment_match else None


# ----------------------------------------
# Step 9: Extract official total from receipt
# ----------------------------------------
# Regex explanation:
# ИТОГО:       -> literal text marking the final total
# \n           -> next line
# ([\d\s]+,\d{2}) -> capture the price value
official_total_pattern = r"ИТОГО:\n([\d\s]+,\d{2})"

official_total_match = re.search(official_total_pattern, text)

official_total = clean_price(official_total_match.group(1)) if official_total_match else None


# ----------------------------------------
# Step 10: Create structured output
# ----------------------------------------
# We organize the parsed data into a dictionary.
# This structure makes the data easy to store, analyze, or convert to JSON.
data = {
    "products": products,
    "item_totals": item_totals,
    "prices_found": prices,
    "calculated_total": calculated_total,
    "official_total": official_total,
    "payment_method": payment_method,
    "datetime": datetime
}


# ----------------------------------------
# Step 11: Output results
# ----------------------------------------
# ensure_ascii=False keeps Cyrillic characters readable
# indent=4 formats the JSON for better readability
print(json.dumps(data, indent=4, ensure_ascii=False))