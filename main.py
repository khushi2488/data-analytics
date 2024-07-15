import fitz  # PyMuPDF
import pandas as pd
import re
import os

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def parse_order_details(text):
    order_number = re.search(r'Order Number\s*(\S+)', text).group(1).strip()
    order_date = re.search(r'Order Date\s*(\d{2}-\d{2}-\d{4})', text).group(1).strip()
    order_status = re.search(r'Order Status\s*(.*)', text).group(1).strip()
    invoice_number_match = re.search(r'Invoice Number:\s*(\S+)', text)
    invoice_number = invoice_number_match.group(1).strip() if invoice_number_match else None

    purchased_by_match  = re.search(r'Purchased By\s*(.*)\nID:', text)
    purchased_by = purchased_by_match.group(1).strip()if purchased_by_match else None

    ship_to_match = re.search(r'Ship To\s*(.*?)(?=Shipping Method)', text, re.DOTALL)
    ship_to = ship_to_match.group(1).strip() if ship_to_match else None
    amount_paid_match = re.search(r'Amount Paid\s*₹ ([\d,]+.\d{2})', text)
    amount_paid =amount_paid_match.group(1).strip() if amount_paid_match else None

    grand_total_match = re.search(r'Grand Total :\s*₹ ([\d,]+.\d{2})', text)
    grand_total = grand_total_match.group(1).strip if grand_total_match else None
    # invoice_number=0

    # Extract discount information
    discount_match = re.search(r'Discount\s*(\d{2} %)', text)
    discount = discount_match.group(1).strip() if discount_match else None

    delivery_charges_match = re.search(r'Delivery Charges:\s*₹\s*([\d,]+.\d{2})', text)
    delivery_charges = delivery_charges_match.group(1) if delivery_charges_match else None
    # delivery_charges=0

    # Extract item details
    item_pattern = re.compile(r'(?:ITEM\s+)?\s+(\d+)\s+((?:[A-Z][A-Z0-9 -]+\s*)+)SKU\s*(\w+)\s*\(Product\)',re.DOTALL)
    items = item_pattern.findall(text)

    # Clean up item names (remove extra spaces)
    items = [(qty, ' '.join(name.split()), sku) for qty, name, sku in items]

    return order_number,delivery_charges, order_date, order_status, invoice_number, purchased_by, ship_to, amount_paid, grand_total, discount, items

def create_dataframe(order_number,delivery_charges, order_date, order_status, invoice_number, purchased_by, ship_to, amount_paid, grand_total, discount, items):
    data = []
    for item in items:
        quantity_shipped, item_name, sku = item
        data.append([
            order_number,delivery_charges, order_date, order_status, invoice_number, purchased_by, ship_to,
            amount_paid, grand_total, discount, quantity_shipped, item_name, sku
        ])

    columns = [
        'Order Number','Delivery Charges', 'Order Date', 'Order Status', 'Invoice Number', 'Purchased By', 'Ship To',
        'Amount Paid', 'Grand Total', 'Discount', 'Quantity Shipped', 'Item', 'SKU'
    ]
    df = pd.DataFrame(data, columns=columns)
    return df

# Directory containing all PDFs
pdf_directory = r'C:\Users\DELL\Downloads\drive-download-20240704T111612Z-0013333'

# Initialize an empty list to collect all DataFrames
all_dfs = []

# Iterate through each PDF file in the directory
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)

        # Extract text from PDF
        text = extract_text_from_pdf(pdf_path)

        # Parse order details
        order_number,delivery_charges, order_date, order_status, invoice_number, purchased_by, ship_to, amount_paid, grand_total, discount, items = parse_order_details(text)



        # Create DataFrame
        df = create_dataframe(order_number,delivery_charges, order_date, order_status, invoice_number, purchased_by, ship_to, amount_paid, grand_total, discount, items)

        # Append DataFrame to the list
        all_dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
if all_dfs:
    combined_df = pd.concat(all_dfs, ignore_index=True)

    # Save to CSV
    output_csv_path = r'C:\Users\DELL\Downloads\pdfs\sep_23.csv'

    combined_df.to_csv(output_csv_path, index=False)
    print(f"Data saved to {output_csv_path}")
else:
    print("No PDF files found or no data extracted.")