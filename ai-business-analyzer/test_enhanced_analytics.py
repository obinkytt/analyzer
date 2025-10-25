#!/usr/bin/env python3
"""
Test script to verify enhanced business analytics functionality
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.analyzer import analyze_text

def test_enhanced_analytics():
    print("Testing Enhanced Business Analytics...")
    print("=" * 50)
    
    # Test with a comprehensive business description
    test_text = """
    TechFlow Solutions is a leading software development company specializing in 
    enterprise SaaS platforms and mobile applications. We serve Fortune 500 companies 
    and growing businesses with innovative digital transformation solutions.
    
    Our services include custom software development, cloud migration, API integrations,
    and digital strategy consulting. With over 10 years of experience and a team of 
    certified developers, we have successfully delivered 200+ projects.
    
    We offer flexible pricing packages, from startup-friendly solutions to enterprise
    licensing deals. Our award-winning customer support and proven track record make
    us the trusted technology partner for businesses worldwide.
    
    Features: automation platforms, secure cloud infrastructure, mobile-first design,
    data analytics, AI-powered recommendations, and seamless third-party integrations.
    """
    
    test_meta = {
        "title": "TechFlow Solutions - Enterprise Software Development",
        "description": "Leading SaaS development company serving Fortune 500 clients",
        "og": {
            "og:title": "TechFlow Solutions",
            "og:description": "Enterprise software development experts"
        },
        "h1": ["Welcome to TechFlow", "Our Services", "Why Choose Us"],
        "h2": ["Software Development", "Cloud Solutions", "Customer Success"]
    }
    
    # Analyze with enhanced business insights
    result = analyze_text(test_text, test_meta)
    
    print(f"📊 BUSINESS OVERVIEW")
    print(f"Industry: {result.industry}")
    print(f"Target Audience: {result.target_audience}")
    print(f"Overall Business Score: {result.overall_business_score}/100")
    print(f"Growth Readiness: {result.readiness_for_growth}")
    print()
    
    if result.business_insights:
        print(f"💼 BUSINESS INSIGHTS")
        print(f"Market Positioning: {result.business_insights.market_positioning}")
        print(f"Digital Maturity Score: {result.business_insights.digital_maturity_score}/10")
        print(f"Revenue Streams: {result.business_insights.revenue_streams}")
        print(f"Competitive Advantages: {result.business_insights.competitive_advantages}")
        print()
    
    if result.marketing_analytics:
        print(f"📈 MARKETING ANALYTICS")
        print(f"Brand Presence Score: {result.marketing_analytics.brand_presence_score}/10")
        print(f"Content Quality Score: {result.marketing_analytics.content_quality_score}/10")
        print(f"UX Score: {result.marketing_analytics.user_experience_score}/10")
        print(f"Social Proof: {result.marketing_analytics.social_proof_indicators}")
        print()
    
    if result.technical_analytics:
        print(f"⚙️ TECHNICAL ANALYTICS")
        print(f"Website Performance: {result.technical_analytics.website_performance_score}/10")
        print(f"Mobile Optimization: {result.technical_analytics.mobile_optimization}")
        print(f"Security Indicators: {result.technical_analytics.security_indicators}")
        print()
    
    print(f"🎯 STRATEGIC RECOMMENDATIONS")
    print(f"Strategic Priorities: {result.strategic_priorities}")
    print(f"Quick Wins: {result.quick_wins}")
    print(f"Investment Recommendations: {result.investment_recommendations}")
    print()
    
    print(f"🚀 DIGITAL TRANSFORMATION")
    print(f"Transformation Needs: {result.digital_transformation_needs}")
    
    return True

if __name__ == "__main__":
    try:
        test_enhanced_analytics()
        print("\n✅ Enhanced business analytics test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)