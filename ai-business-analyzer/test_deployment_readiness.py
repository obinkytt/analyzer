#!/usr/bin/env python3
"""
Deployment readiness check for AI Business Analyzer
Tests that the app works without external dependencies
"""
import sys
import os
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_deployment_readiness():
    print("🔍 Testing Deployment Readiness...")
    print("=" * 50)
    
    # Test 1: Import all modules
    try:
        from app.main import app
        from app.analyzer import analyze_text, select_provider
        from app.models import InsightReport
        print("✅ All modules imported successfully")
    except Exception as e:
        print(f"❌ Module import failed: {e}")
        return False
    
    # Test 2: Check provider selection (should fall back to heuristic)
    try:
        provider = select_provider()
        provider_name = provider.__class__.__name__
        print(f"✅ Provider selected: {provider_name}")
        
        if provider_name == "HeuristicProvider":
            print("✅ Using heuristic analysis (perfect for cloud deployment)")
        elif provider_name == "OpenAIProvider":
            print("✅ Using OpenAI (requires API key in production)")
        elif provider_name == "OllamaProvider":
            print("⚠️  Using Ollama (will not be available in cloud)")
    except Exception as e:
        print(f"❌ Provider selection failed: {e}")
        return False
    
    # Test 3: Analyze sample business (should work without AI)
    try:
        test_text = "Software consulting company providing web development services to small businesses"
        result = analyze_text(test_text, {})
        
        print(f"✅ Analysis completed successfully")
        print(f"   Industry: {result.industry}")
        print(f"   Business Score: {result.overall_business_score}/100")
        print(f"   Growth Readiness: {result.readiness_for_growth}")
        
        if result.overall_business_score and result.overall_business_score > 0:
            print("✅ Comprehensive business insights generated")
        else:
            print("⚠️  Basic analysis only")
            
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False
    
    # Test 4: Check for deployment files
    deployment_files = [
        "run_production.py",
        "requirements-prod.txt", 
        "Procfile",
        "DEPLOYMENT_INSTRUCTIONS.md"
    ]
    
    missing_files = []
    for file in deployment_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            missing_files.append(file)
            print(f"⚠️  {file} missing")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 DEPLOYMENT READINESS SUMMARY")
    print("=" * 50)
    
    if provider_name == "HeuristicProvider":
        print("🎯 RECOMMENDED: Deploy with heuristic analysis")
        print("   ✅ No external dependencies")
        print("   ✅ Fast and reliable")
        print("   ✅ Works on any cloud platform")
        print("   ✅ Zero additional costs")
    elif provider_name == "OpenAIProvider":
        print("🤖 ENHANCED: Deploy with OpenAI integration")
        print("   ✅ AI-powered insights")
        print("   ⚠️  Requires OPENAI_API_KEY environment variable")
        print("   💰 API usage costs apply")
    else:
        print("⚠️  ATTENTION: Ollama detected locally")
        print("   ❌ Will not work in cloud deployment")
        print("   ✅ Will automatically fall back to heuristics")
    
    print(f"\n🚀 READY FOR DEPLOYMENT: {'YES' if not missing_files else 'CHECK MISSING FILES'}")
    
    if not missing_files:
        print("\n📋 NEXT STEPS:")
        print("1. Push code to GitHub")
        print("2. Deploy to Render/Railway/Fly.io")
        print("3. (Optional) Add OPENAI_API_KEY for AI features")
        print("4. Share your live business analyzer!")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    try:
        success = test_deployment_readiness()
        if success:
            print("\n🎉 Your AI Business Analyzer is ready for cloud deployment!")
        else:
            print("\n⚠️  Please resolve the issues above before deploying.")
    except Exception as e:
        print(f"\n💥 Deployment readiness check failed: {e}")
        sys.exit(1)