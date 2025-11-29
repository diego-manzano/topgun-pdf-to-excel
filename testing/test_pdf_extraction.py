#!/usr/bin/env python3
"""
Test PDF extraction with Gemini Vision API
"""

import os
import json
import base64
from pathlib import Path
import google.generativeai as genai

EXTRACTION_PROMPT = """
Extract all transaction data from this Petron Merchant Settlement Report PDF.
Focus on the transaction table (usually on page 1).

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
- Extract ALL transaction rows from the table
- Parse numbers correctly (remove commas from amounts)
- Keep dates in their original format
- Only return valid JSON, no markdown code blocks or extra text
"""

def test_pdf_extraction():
    api_key = 'AIzaSyCWS2QfciN2Zyqpgx4zaWNr1Pqwf2APBe4'
    if not api_key:
        print("❌ GEMINI_API_KEY not set!")
        return
    
    genai.configure(api_key=api_key)
    
    # Use gemini-2.5-flash which supports PDFs
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Load PDF - try multiple locations
    possible_paths = [
        Path("PFC Nov 3 2025 (1).pdf"),
        Path("test.pdf"),
        Path("petron_report.pdf"),
    ]
    
    pdf_path = None
    for path in possible_paths:
        if path.exists():
            pdf_path = path
            break
    
    if not pdf_path:
        print("❌ PDF not found!")
        print("\nSearched in:")
        for path in possible_paths:
            print(f"   - {path.absolute()}")
        print("\nPlease copy your PDF to the current directory")
        return
    
    print("🧪 PDF Extraction Test")
    print("=" * 80)
    print(f"📄 Loading PDF: {pdf_path}")
    
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
    
    print(f"   Size: {len(pdf_bytes) / 1024:.1f} KB")
    print()
    print("🤖 Calling Gemini Vision API...")
    print()
    
    # Send PDF to Gemini
    response = model.generate_content([
        EXTRACTION_PROMPT,
        {
            "mime_type": "application/pdf",
            "data": pdf_bytes
        }
    ])
    
    print("📥 Raw Response:")
    print("=" * 80)
    print(response.text)
    print("=" * 80)
    print()
    
    # Parse JSON
    try:
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
        
        # Validation
        expected_transactions = 17
        actual_transactions = len(data['transactions'])
        
        print("🔍 Validation:")
        if actual_transactions == expected_transactions:
            print(f"   ✅ Transaction count: {actual_transactions}/{expected_transactions}")
        else:
            print(f"   ⚠️  Transaction count: {actual_transactions}/{expected_transactions}")
        
        # Check totals
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
        
        # Save output
        output_path = Path("extracted_from_pdf.json")
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n💾 Saved to: {output_path}")
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON: {e}")
    except KeyError as e:
        print(f"❌ Missing key: {e}")

if __name__ == "__main__":
    test_pdf_extraction()