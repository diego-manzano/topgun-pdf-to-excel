#!/usr/bin/env python3
import os
import google.generativeai as genai

api_key = 'AIzaSyCWS2QfciN2Zyqpgx4zaWNr1Pqwf2APBe4'
if not api_key:
    print("Set GEMINI_API_KEY first!")
    exit(1)

genai.configure(api_key=api_key)

print("Available Gemini models:")
print("=" * 80)
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"\n📦 {model.name}")
        print(f"   Description: {model.description}")
        print(f"   Methods: {model.supported_generation_methods}")