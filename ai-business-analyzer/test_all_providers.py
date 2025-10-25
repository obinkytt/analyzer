#!/usr/bin/env python3
"""
Test all analysis providers to ensure they work correctly
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from analyzer import get_analyzer
from models import SiteContent

# Load environment variables
load_dotenv()

async def test_provider(provider_name):
    """Test a specific analysis provider"""
    print(f"\n🔍 Testing {provider_name.upper()} provider...")
    
    # Temporarily set the provider
    original_provider = os.environ.get('ANALYSIS_PROVIDER')
    os.environ['ANALYSIS_PROVIDER'] = provider_name
    
    try:
        # Create test data
        test_content = SiteContent(
            url="https://example.com",
            title="Example Business Website",
            description="A sample business website for testing",
            content="This is a test business website with great products and services. We focus on customer satisfaction and innovation.",
            meta={"keywords": "business, products, services"},
            links=["https://example.com/about", "https://example.com/contact"]
        )
        
        # Get analyzer and test
        analyzer = get_analyzer()
        result = await analyzer.analyze(test_content)
        
        print(f"✅ {provider_name.upper()} - Analysis successful!")
        print(f"   Overall Score: {result.overall_score}/100")
        print(f"   Business Insights: {len(result.business_insights.strengths)} strengths, {len(result.business_insights.weaknesses)} weaknesses")
        print(f"   Provider: {result.provider}")
        
        return True
        
    except Exception as e:
        print(f"❌ {provider_name.upper()} - Error: {str(e)}")
        return False
        
    finally:
        # Restore original provider
        if original_provider:
            os.environ['ANALYSIS_PROVIDER'] = original_provider
        elif 'ANALYSIS_PROVIDER' in os.environ:
            del os.environ['ANALYSIS_PROVIDER']

async def main():
    """Test all providers"""
    print("🧪 Testing All Analysis Providers")
    print("=" * 50)
    
    providers = ['heuristic', 'openai', 'ollama']
    results = {}
    
    for provider in providers:
        results[provider] = await test_provider(provider)
    
    print("\n📊 Test Results Summary")
    print("=" * 30)
    for provider, success in results.items():
        status = "✅ Working" if success else "❌ Failed"
        print(f"{provider.upper():<12}: {status}")
    
    print(f"\n💡 Current provider in .env: {os.getenv('ANALYSIS_PROVIDER', 'heuristic')}")
    
    # Recommendations
    working_providers = [p for p, success in results.items() if success]
    if working_providers:
        print(f"\n🎯 Available providers: {', '.join(working_providers)}")
        print("\n🔄 To switch providers, edit your .env file:")
        for provider in working_providers:
            print(f"   ANALYSIS_PROVIDER={provider}")

if __name__ == "__main__":
    asyncio.run(main())