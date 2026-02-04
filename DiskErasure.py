import os
from pathlib import Path
from pypdf import PdfReader
from escpos.printer import Usb
from PIL import Image

# ================== CONFIG ==================
VENDOR_ID = 0x04b8                             # Epson USB vendor ID
PRODUCT_ID = 0x0e28                            # Epson USB product ID (change if needed)
LOGO_PATH = "TAZW-Logo.png"                    # Path to logo for receipts               # 58mm printer width in pixels
# ============================================

# ---------- PDF Parsing Utilities ----------
def remove_duplicate_lines(text):
    """Remove duplicate lines from text and strip whitespace."""
    lines = text.splitlines()
    seen = set()
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line and line not in seen:
            clean_lines.append(line)
            seen.add(line)
    return clean_lines

def extract_killdisk_pdf(pdf_path):
    """
    Extract disk and hardware info from a KillDisk certificate PDF.
    Handles keys and values on separate lines.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"

    lines = remove_duplicate_lines(text)
    data = {"disk": {}, "hardware": {}}

    # Keys without colon for mapping
    mapping = {
        "Device Name": "disk",
        "Product Name": "disk",
        "Serial Number": "disk",
        "Erase Method": "disk",
        "Verification": "disk",
        "Erase Range": "disk",
        "Started": "disk",
        "Duration": "disk",
        "Status": "disk",
        "OS": "hardware",
        "Type": "hardware",
        "Manufacturer": "hardware",
        "Description": "hardware",
        "Logical Processors": "hardware",
        "Memory": "hardware",
        "Name": "hardware",
        "System": "hardware",
        "Physical Processors": "hardware"
    }

    current_key = None
    for line in lines:
        line_clean = line.strip().rstrip(":")  # remove trailing colon
        if line_clean in mapping:
            current_key = line_clean
        elif current_key:
            category = mapping[current_key]
            data[category][current_key] = line_clean
            current_key = None

    print(data)
    return data


# ---------- Printer Utilities ----------
def test_printer_connection(vendor_id, product_id):
    """Attempt to connect to Epson USB printer."""
    try:
        printer = Usb(vendor_id, product_id)
        return printer
    except Exception as e:
        print("Printer connection failed:", e)
        return None

def print_killdisk_receipt(printer, data, logo_path=LOGO_PATH):
    """Print KillDisk certificate receipt to the connected printer."""
    # Print logo
    try:
        logo = Image.open(LOGO_PATH)
        printer.image(logo)
    except Exception as e:
        print("Logo print failed:", e)

    printer.text("\n")
    printer.set(align="center", bold=True)
    printer.text("DISK ERASURE CERTIFICATE\n")
    printer.text("========================\n\n")

    # Disk info
    printer.set(align="left", bold=True)
    printer.text("DISK INFORMATION\n")
    printer.set(bold=False)
    for k, v in data["disk"].items():
        printer.text(f"{k}: {v}\n")

    printer.text("\n")
    # Hardware info
    printer.set(bold=True)
    printer.text("HARDWARE\n")
    printer.set(bold=False)
    for k, v in data["hardware"].items():
        printer.text(f"{k}: {v}\n")

    printer.text("\n")
    printer.set(align="center")
    printer.text("Erased using Active@ KillDisk\n")
    printer.text("========================\n")

    printer.text("\n\n\n")
    printer.cut()
