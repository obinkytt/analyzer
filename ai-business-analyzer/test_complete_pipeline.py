#!/usr/bin/env python3
"""
Test script to verify the complete scraping and analysis pipeline
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.scraper import extract_text_and_metadata
from app.analyzer import analyze_text

def test_complete_pipeline():
    print("Testing complete scraping and analysis pipeline...")
    
    # Simulate HTML content that would cause the original error
    test_html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Example Business Website</title>
        <meta name="description" content="We provide excellent business services">
        <meta name="keywords" content="business, services, consulting">
        <meta property="og:locale" content="en_US">
        <meta property="og:title" content="Example Business">
        <meta property="og:description" content="Professional business services">
        <meta property="og:type" content="website">
        <meta property="og:image" content="https://example.com/image.jpg">
        <meta property="og:image:type" content="image/jpeg">
    </head>
    <body>
        <h1>Welcome to Our Business</h1>
        <h2>Our Services</h2>
        <p>We offer comprehensive business consulting services to help your company grow.</p>
        <h2>About Us</h2>
        <p>With over 20 years of experience, we provide expert guidance for businesses.</p>
        <a href="/contact">Contact Us</a>
        <a href="/services">View Services</a>
    </body>
    </html>
    '''
    
    try:
        # Step 1: Extract content and metadata (this was causing the error)
        print("1. Extracting content and metadata...")
        content = extract_text_and_metadata(test_html, "https://example.com")
        print(f"   ✅ Content extracted successfully")
        print(f"   Text length: {len(content.text)} chars")
        print(f"   Meta keys: {list(content.meta.keys())}")
        print(f"   OG metadata: {content.meta.get('og', {})}")
        
        # Step 2: Analyze the content (this should now work)
        print("\n2. Analyzing content...")
        result = analyze_text(content.text, content.meta)
        print(f"   ✅ Analysis completed successfully")
        print(f"   Industry: {result.industry}")
        print(f"   Target Audience: {result.target_audience}")
        print(f"   Key Products: {result.key_products}")
        print(f"   Report: {result.report_text}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Pipeline test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_complete_pipeline()
    if success:
        print("\n🎉 Complete pipeline test successful!")
        print("The SiteContent validation error has been fixed!")
    else:
        print("\n💥 Pipeline test failed!")
        sys.exit(1)