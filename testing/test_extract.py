#!/usr/bin/env python3
"""
Test script to validate Gemini Vision extraction for Petron Settlement Reports
"""

import os
import json
import base64
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("Installing google-generativeai...")
    os.system("pip install google-generativeai --break-system-packages -q")
    import google.generativeai as genai

EXTRACTION_PROMPT = """
Extract all data from this Petron Merchant Settlement Report image.
Return as JSON with this exact structure:
{
  "header": {
    "customer_number": "",
    "business_location_id": "",
    "business_location_name": "",
    "date_from": "",
    "date_to": "",
    "reimbursement_batch": ""
  },
  "transactions": [
    {
      "terminal_id": "",
      "host_batch_id": "",
      "ids": "",
      "settle_date": "",
      "no_of_txn": 0,
      "gross_amount": 0.00,
      "ewt": 0.00,
      "net_amount": 0.00,
      "description": ""
    }
  ],
  "totals": {
    "gross_amount": 0.00,
    "ewt": 0.00,
    "net_amount": 0.00
  }
}

Important:
- Extract ALL transaction rows visible in the table
- Parse numbers correctly (remove commas from amounts)
- Keep dates in their original format
- Only return valid JSON, no markdown code blocks or extra text
"""

def test_extraction():
    # Check for API key
    api_key = 'AIzaSyCWS2QfciN2Zyqpgx4zaWNr1Pqwf2APBe4'
    if not api_key:
        print("❌ GEMINI_API_KEY environment variable not set!")
        print("\nTo get your API key:")
        print("1. Go to https://aistudio.google.com/")
        print("2. Click 'Get API Key'")
        print("3. Create a new key or use an existing one")
        print("4. Run: export GEMINI_API_KEY='your-key-here'")
        return
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Load image
    image_path = Path("test_image.png")
    if not image_path.exists():
        print(f"❌ Image not found at {image_path}")
        return
    
    print("📸 Loading image...")
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    print("🤖 Calling Gemini Vision API...")
    print(f"   Model: gemini-1.5-flash")
    print(f"   Image size: {len(image_bytes) / 1024:.1f} KB")
    print()
    
    # Generate content
    response = model.generate_content([
        EXTRACTION_PROMPT,
        {
            "mime_type": "image/png",
            "data": image_bytes
        }
    ])
    
    print("📥 Raw Response:")
    print("=" * 80)
    print(response.text)
    print("=" * 80)
    print()
    
    # Try to parse as JSON
    try:
        # Clean up potential markdown code blocks
        response_text = response.text.strip()
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        data = json.loads(response_text)
        
        print("✅ Successfully parsed JSON!")
        print()
        print("📊 Extraction Summary:")
        print(f"   Customer: {data['header']['customer_number']}")
        print(f"   Business: {data['header']['business_location_name']}")
        print(f"   Period: {data['header']['date_from']} to {data['header']['date_to']}")
        print(f"   Batch: {data['header']['reimbursement_batch']}")
        print(f"   Transactions: {len(data['transactions'])}")
        print(f"   Total Gross: ₱{data['totals']['gross_amount']:,.2f}")
        print(f"   Total EWT: ₱{data['totals']['ewt']:,.2f}")
        print(f"   Total Net: ₱{data['totals']['net_amount']:,.2f}")
        print()
        
        # Show first few transactions
        print("🔍 Sample Transactions (first 3):")
        for i, txn in enumerate(data['transactions'][:3], 1):
            print(f"\n   Transaction {i}:")
            print(f"      Terminal: {txn['terminal_id']}")
            print(f"      Date: {txn['settle_date']}")
            print(f"      Count: {txn['no_of_txn']}")
            print(f"      Gross: ₱{txn['gross_amount']:,.2f}")
            print(f"      Net: ₱{txn['net_amount']:,.2f}")
        
        # Save extracted data
        output_path = Path("/home/claude/extracted_data.json")
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n💾 Full data saved to: {output_path}")
        
        # Validation checks
        print("\n🔍 Validation Checks:")
        expected_transactions = 17  # From the document
        actual_transactions = len(data['transactions'])
        if actual_transactions == expected_transactions:
            print(f"   ✅ Transaction count: {actual_transactions}/{expected_transactions}")
        else:
            print(f"   ⚠️  Transaction count: {actual_transactions}/{expected_transactions} (mismatch)")
        
        # Check if totals match
        expected_gross = 178570.28
        expected_ewt = 1594.43
        expected_net = 176975.85
        
        gross_match = abs(data['totals']['gross_amount'] - expected_gross) < 0.01
        ewt_match = abs(data['totals']['ewt'] - expected_ewt) < 0.01
        net_match = abs(data['totals']['net_amount'] - expected_net) < 0.01
        
        if gross_match and ewt_match and net_match:
            print(f"   ✅ Totals match expected values")
        else:
            print(f"   ⚠️  Totals mismatch:")
            if not gross_match:
                print(f"      Gross: {data['totals']['gross_amount']:,.2f} vs {expected_gross:,.2f}")
            if not ewt_match:
                print(f"      EWT: {data['totals']['ewt']:,.2f} vs {expected_ewt:,.2f}")
            if not net_match:
                print(f"      Net: {data['totals']['net_amount']:,.2f} vs {expected_net:,.2f}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {e}")
        print("\nThe model might have returned markdown or extra text.")
        print("We may need to adjust the prompt to be more explicit about JSON-only output.")
    except KeyError as e:
        print(f"❌ Missing expected key in response: {e}")
        print("\nThe response structure doesn't match what we expected.")

if __name__ == "__main__":
    print("🧪 Gemini Vision Extraction Test")
    print("=" * 80)
    print()
    test_extraction()