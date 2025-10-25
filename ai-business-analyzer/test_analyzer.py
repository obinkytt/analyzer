#!/usr/bin/env python3
"""
Test script to verify analyzer functionality without environment
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.analyzer import analyze_text

def test_analysis():
    # Test 1: Software company
    print("=== Test 1: Software Company ===")
    result = analyze_text(
        "Software development company specializing in web applications and mobile apps for small businesses",
        {}
    )
    print(f"Industry: {result.industry}")
    print(f"Target Audience: {result.target_audience}")
    print(f"Report: {result.report_text}")
    print()

    # Test 2: Healthcare
    print("=== Test 2: Healthcare Clinic ===")
    result = analyze_text(
        "Family health clinic providing comprehensive medical care including pediatrics, geriatrics, and preventive medicine",
        {"title": "ABC Health Clinic", "description": "Your trusted healthcare provider"}
    )
    print(f"Industry: {result.industry}")
    print(f"Target Audience: {result.target_audience}")
    print(f"Key Products: {result.key_products}")
    print(f"Report: {result.report_text}")
    print()

    # Test 3: E-commerce
    print("=== Test 3: E-commerce Store ===")
    result = analyze_text(
        "Online shop selling handmade jewelry and accessories with shopping cart and secure checkout",
        {"title": "Artisan Jewelry Store", "h1": ["Featured Products", "About Our Craft"]}
    )
    print(f"Industry: {result.industry}")
    print(f"Target Audience: {result.target_audience}")
    print(f"Opportunities: {result.growth_opportunities}")
    print(f"Report: {result.report_text}")

if __name__ == "__main__":
    print("Testing AI Business Analyzer without environment setup...")
    print("This will use the heuristic fallback analyzer.")
    print()
    test_analysis()
    print("\n=== Tests completed successfully! ===")