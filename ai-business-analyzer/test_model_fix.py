#!/usr/bin/env python3
"""
Test script to verify the SiteContent model fix
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import SiteContent

def test_site_content_model():
    print("Testing SiteContent model with og metadata...")
    
    # This is the type of data structure that caused the error
    test_meta = {
        "title": "Example Website",
        "description": "A test website description",
        "keywords": "test, example, website",
        "og": {
            "og:locale": "en_US",
            "og:title": "Example Site",
            "og:description": "Test description",
            "og:type": "website",
            "og:image": "https://example.com/image.jpg",
            "og:image:type": "image/jpeg"
        },
        "h1": ["Main Heading", "Secondary Heading"],
        "h2": ["Subheading 1", "Subheading 2"]
    }
    
    try:
        # This should now work without validation errors
        content = SiteContent(
            url="https://example.com",
            text="Sample website content text here",
            meta=test_meta,
            links=["https://example.com/about", "https://example.com/contact"]
        )
        
        print("✅ SiteContent model validation successful!")
        print(f"   URL: {content.url}")
        print(f"   Text length: {len(content.text)} chars")
        print(f"   Meta keys: {list(content.meta.keys())}")
        print(f"   OG data type: {type(content.meta['og'])}")
        print(f"   Links count: {len(content.links)}")
        return True
        
    except Exception as e:
        print(f"❌ SiteContent model validation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_site_content_model()
    if success:
        print("\n🎉 Model fix verified successfully!")
    else:
        print("\n💥 Model fix failed!")
        sys.exit(1)