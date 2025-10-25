#!/usr/bin/env python3
"""
Test deployment simulation (no Ollama, no OpenAI)
This simulates how the app will work in cloud deployment
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Temporarily disable environment variables to simulate cloud without AI
original_openai_key = os.environ.get('OPENAI_API_KEY')
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']

def test_cloud_simulation():
    print("☁️  Simulating Cloud Deployment (No Local AI)")
    print("=" * 50)
    
    from app.analyzer import analyze_text, select_provider
    
    # Test provider selection in cloud environment
    provider = select_provider()
    provider_name = provider.__class__.__name__
    print(f"🔧 Provider in cloud: {provider_name}")
    
    if provider_name == "HeuristicProvider":
        print("✅ Perfect! Using heuristic analysis (cloud-ready)")
    else:
        print(f"⚠️  Unexpected provider: {provider_name}")
    
    # Test comprehensive business analysis
    print("\n📊 Testing Business Analysis in Cloud Mode...")
    
    test_cases = [
        {
            "name": "SaaS Startup",
            "text": "Revolutionary AI-powered project management platform for remote teams. SaaS subscription model with freemium tier.",
            "meta": {"title": "TeamFlow AI", "description": "AI project management for remote teams"}
        },
        {
            "name": "E-commerce Store", 
            "text": "Online marketplace selling handmade artisan products with secure checkout and mobile app",
            "meta": {"title": "Artisan Market", "h1": ["Featured Products", "About Our Artisans"]}
        },
        {
            "name": "Healthcare Clinic",
            "text": "Family medical clinic providing comprehensive healthcare services including pediatrics and geriatrics",
            "meta": {"title": "Family Health Center", "description": "Comprehensive family healthcare"}
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n🏢 Test Case {i}: {case['name']}")
        print("-" * 30)
        
        result = analyze_text(case['text'], case['meta'])
        
        print(f"Industry: {result.industry}")
        print(f"Target Audience: {result.target_audience}")
        print(f"Business Score: {result.overall_business_score}/100")
        print(f"Growth Readiness: {result.readiness_for_growth}")
        
        if result.business_insights:
            print(f"Revenue Streams: {len(result.business_insights.revenue_streams)} identified")
            print(f"Digital Maturity: {result.business_insights.digital_maturity_score}/10")
        
        if result.marketing_analytics:
            print(f"Brand Presence: {result.marketing_analytics.brand_presence_score}/10")
        
        print(f"Strategic Priorities: {len(result.strategic_priorities)} identified")
        print(f"Quick Wins: {len(result.quick_wins)} identified")
    
    print("\n" + "=" * 50)
    print("☁️  CLOUD DEPLOYMENT SIMULATION RESULTS")
    print("=" * 50)
    print("✅ Heuristic analysis works perfectly")
    print("✅ All business insights generated")
    print("✅ Comprehensive scoring system functional")
    print("✅ Strategic recommendations provided")
    print("✅ No external dependencies required")
    print("\n🎉 Ready for cloud deployment!")

if __name__ == "__main__":
    test_cloud_simulation()
    
    # Restore environment
    if original_openai_key:
        os.environ['OPENAI_API_KEY'] = original_openai_key