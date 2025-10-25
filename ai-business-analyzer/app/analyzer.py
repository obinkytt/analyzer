from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import httpx
from pydantic import BaseModel
from dotenv import load_dotenv

from .models import InsightReport, SiteContent, BusinessInsights, MarketingAnalytics, TechnicalAnalytics

load_dotenv()


@dataclass
class ProviderResult:
    ok: bool
    text: str


class BaseProvider:
    def available(self) -> bool:
        raise NotImplementedError

    def generate(self, prompt: str) -> ProviderResult:
        raise NotImplementedError


class OpenAIProvider(BaseProvider):
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def available(self) -> bool:
        return bool(self.api_key)

    def generate(self, prompt: str) -> ProviderResult:
        try:
            from openai import OpenAI  # type: ignore

            client = OpenAI(api_key=self.api_key)
            resp = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business analysis assistant. Reply in concise JSON unless asked for prose."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
            )
            text = resp.choices[0].message.content or ""
            return ProviderResult(True, text)
        except Exception as e:
            return ProviderResult(False, f"OpenAI error: {e}")


class OllamaProvider(BaseProvider):
    def __init__(self) -> None:
        self.base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

    def available(self) -> bool:
        try:
            # Quick health check
            r = httpx.get(self.base, timeout=1.0)
            return r.status_code < 500
        except Exception:
            return False

    def generate(self, prompt: str) -> ProviderResult:
        try:
            r = httpx.post(
                f"{self.base}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False, "options": {"temperature": 0.2}},
                timeout=60.0,
            )
            r.raise_for_status()
            data = r.json()
            return ProviderResult(True, data.get("response", ""))
        except Exception as e:
            return ProviderResult(False, f"Ollama error: {e}")


class HeuristicProvider(BaseProvider):
    def available(self) -> bool:
        # Always available as fallback
        return True

    def generate(self, prompt: str) -> ProviderResult:
        # Not used directly; we'll call helper below
        return ProviderResult(True, "")

    @staticmethod
    def analyze(text: str, meta: Dict[str, Any]) -> InsightReport:
        lowered = text.lower()
        title = (meta.get("title") or "") if isinstance(meta, dict) else ""
        description = (meta.get("description") or "") if isinstance(meta, dict) else ""
        keywords = (meta.get("keywords") or "") if isinstance(meta, dict) else ""

        # Naive keyword cues
        industry = None
        if any(k in lowered for k in ["clinic", "health", "hospital", "care"]):
            industry = "Healthcare"
        elif any(k in lowered for k in ["software", "saas", "platform", "api"]):
            industry = "Software / SaaS"
        elif any(k in lowered for k in ["shop", "store", "cart", "ecommerce", "e-commerce"]):
            industry = "E-commerce"
        elif any(k in lowered for k in ["recruit", "staffing", "talent", "hiring"]):
            industry = "Staffing / Recruiting"
        elif any(k in lowered for k in ["real estate", "realtor", "property"]):
            industry = "Real Estate"
        else:
            industry = "General Business"

        # Extract heading tokens as product hints
        heads = []
        for key in ("h1", "h2"):
            if isinstance(meta, dict) and isinstance(meta.get(key), list):
                heads.extend(meta.get(key) or [])
        # Simple splitting
        tokens = re.findall(r"[A-Za-z][A-Za-z\-']+", " ".join(heads) + " " + title + " " + description + " " + keywords)
        # Deduplicate, keep meaningful
        seen = set()
        key_products: List[str] = []
        for t in tokens:
            tt = t.strip().lower()
            if len(tt) < 4:
                continue
            if tt in seen:
                continue
            seen.add(tt)
            if tt not in {"about", "services", "solutions", "contact", "learn", "more", "home"}:
                key_products.append(t)
            if len(key_products) >= 8:
                break

        target_audience = None
        if any(k in lowered for k in ["b2b", "enterprise", "businesses", "corporate"]):
            target_audience = "B2B / Enterprises"
        elif any(k in lowered for k in ["students", "parents", "families", "kids"]):
            target_audience = "Consumers / Families"
        elif any(k in lowered for k in ["developer", "engineer", "it team"]):
            target_audience = "Developers / IT"
        else:
            target_audience = "General Audience"

        strengths = []
        if any(k in lowered for k in ["award", "certified", "testimonial", "case study", "trusted"]):
            strengths.append("Trust signals (awards/testimonials)")
        if len(heads) >= 2:
            strengths.append("Clear information hierarchy")
        if len(text) > 2000:
            strengths.append("Rich content depth")

        opportunities = []
        if "blog" not in lowered and "news" not in lowered:
            opportunities.append("Add or improve blog/news content cadence")
        if not keywords:
            opportunities.append("Define meta keywords and semantic coverage")
        if len(text) < 800:
            opportunities.append("Expand on-page copy for SEO")

        # Enhanced Business Analytics
        business_insights = BusinessInsights(
            market_positioning=_analyze_market_positioning(industry, target_audience, text),
            revenue_streams=_identify_revenue_streams(text, industry),
            competitive_advantages=_assess_competitive_advantages(text, strengths),
            risk_factors=_identify_risk_factors(text, industry),
            digital_maturity_score=_calculate_digital_maturity(text, meta),
            customer_acquisition_channels=_identify_acquisition_channels(text),
            pricing_strategy=_analyze_pricing_strategy(text),
            scalability_assessment=_assess_scalability(text, industry)
        )

        marketing_analytics = MarketingAnalytics(
            brand_presence_score=_calculate_brand_presence(text, meta),
            content_quality_score=_assess_content_quality(text, len(heads)),
            user_experience_score=_assess_user_experience(text, meta),
            social_proof_indicators=_find_social_proof(text),
            conversion_optimization_tips=_generate_conversion_tips(text, industry),
            target_demographics=_analyze_demographics(target_audience, text)
        )

        technical_analytics = TechnicalAnalytics(
            website_performance_score=_assess_website_performance(text, meta),
            mobile_optimization=_check_mobile_optimization(meta),
            security_indicators=_assess_security(text),
            technical_debt_areas=_identify_technical_debt(text),
            integration_opportunities=_find_integration_opportunities(text, industry)
        )

        strategic_priorities = _generate_strategic_priorities(industry, text)
        quick_wins = _identify_quick_wins(text, opportunities)
        long_term_goals = _set_long_term_goals(industry, target_audience)
        investment_recommendations = _generate_investment_recommendations(industry, text)

        overall_score = _calculate_overall_business_score(
            business_insights.digital_maturity_score or 5,
            marketing_analytics.brand_presence_score or 5,
            technical_analytics.website_performance_score or 5
        )

        return InsightReport(
            industry=industry,
            key_products=key_products[:8],
            target_audience=target_audience,
            website_strength=", ".join(strengths) or None,
            growth_opportunities=opportunities,
            competitors=[],
            seo_summary=(f"Title: {title[:80]} | Description: {description[:160]}") if (title or description) else None,
            sentiment_summary=None,
            raw_findings={"keyword_sample": key_products[:8]},
            report_text=(
                f"This appears to be a {industry} website targeting {target_audience}. "
                f"Content length: {len(text)} chars. Overall business score: {overall_score}/100."
            ),
            business_insights=business_insights,
            marketing_analytics=marketing_analytics,
            technical_analytics=technical_analytics,
            strategic_priorities=strategic_priorities,
            quick_wins=quick_wins,
            long_term_goals=long_term_goals,
            investment_recommendations=investment_recommendations,
            overall_business_score=overall_score,
            readiness_for_growth=_assess_growth_readiness(overall_score),
            digital_transformation_needs=_identify_digital_transformation_needs(text, industry)
        )


# Enhanced Business Analytics Helper Functions

def _analyze_market_positioning(industry: str, target_audience: str, text: str) -> str:
    """Analyze market positioning based on industry and content"""
    lowered = text.lower()
    if "premium" in lowered or "luxury" in lowered or "exclusive" in lowered:
        return f"Premium {industry} provider targeting {target_audience}"
    elif "affordable" in lowered or "budget" in lowered or "cost-effective" in lowered:
        return f"Cost-competitive {industry} solution for {target_audience}"
    elif "innovative" in lowered or "cutting-edge" in lowered or "advanced" in lowered:
        return f"Innovation-focused {industry} leader for {target_audience}"
    else:
        return f"Established {industry} service provider for {target_audience}"

def _identify_revenue_streams(text: str, industry: str) -> List[str]:
    """Identify potential revenue streams based on content analysis"""
    lowered = text.lower()
    streams = []
    
    if "subscription" in lowered or "monthly" in lowered or "annual" in lowered:
        streams.append("Subscription/Recurring Revenue")
    if "consulting" in lowered or "advisory" in lowered:
        streams.append("Professional Services")
    if "product" in lowered or "sell" in lowered or "buy" in lowered:
        streams.append("Product Sales")
    if "training" in lowered or "course" in lowered or "workshop" in lowered:
        streams.append("Education/Training")
    if "license" in lowered or "partnership" in lowered:
        streams.append("Licensing/Partnerships")
    
    if not streams:
        if industry == "Software / SaaS":
            streams = ["SaaS Subscriptions", "Professional Services"]
        elif industry == "E-commerce":
            streams = ["Product Sales", "Marketplace Commissions"]
        elif industry == "Healthcare":
            streams = ["Service Fees", "Insurance Billing"]
        else:
            streams = ["Service Revenue", "Consultancy"]
    
    return streams

def _assess_competitive_advantages(text: str, strengths: List[str]) -> List[str]:
    """Assess competitive advantages from content"""
    lowered = text.lower()
    advantages = []
    
    if any("award" in s for s in strengths):
        advantages.append("Industry Recognition & Awards")
    if "experience" in lowered or "years" in lowered:
        advantages.append("Established Experience")
    if "team" in lowered or "expert" in lowered:
        advantages.append("Skilled Team & Expertise")
    if "technology" in lowered or "platform" in lowered:
        advantages.append("Advanced Technology Platform")
    if "customer" in lowered or "client" in lowered:
        advantages.append("Strong Customer Relationships")
    
    return advantages or ["Domain Expertise", "Customer Focus"]

def _identify_risk_factors(text: str, industry: str) -> List[str]:
    """Identify potential business risk factors"""
    lowered = text.lower()
    risks = []
    
    if len(text) < 500:
        risks.append("Limited online presence")
    if "contact" not in lowered:
        risks.append("Unclear contact/communication channels")
    
    # Industry-specific risks
    if industry == "Software / SaaS":
        risks.extend(["Technology disruption", "Data security concerns"])
    elif industry == "Healthcare":
        risks.extend(["Regulatory compliance", "Privacy regulations"])
    elif industry == "E-commerce":
        risks.extend(["Market competition", "Supply chain dependencies"])
    else:
        risks.extend(["Market competition", "Economic sensitivity"])
    
    return risks

def _calculate_digital_maturity(text: str, meta: Dict[str, Any]) -> int:
    """Calculate digital maturity score (1-10)"""
    score = 5  # Base score
    lowered = text.lower()
    
    # Positive indicators
    if meta.get("og"):
        score += 1  # Social media optimization
    if "api" in lowered or "integration" in lowered:
        score += 1  # Technical sophistication
    if "mobile" in lowered or "app" in lowered:
        score += 1  # Mobile presence
    if "analytics" in lowered or "data" in lowered:
        score += 1  # Data-driven approach
    if len(text) > 1500:
        score += 1  # Rich digital content
    
    return min(10, max(1, score))

def _identify_acquisition_channels(text: str) -> List[str]:
    """Identify customer acquisition channels"""
    lowered = text.lower()
    channels = []
    
    if "seo" in lowered or "search" in lowered:
        channels.append("Search Engine Optimization")
    if "social" in lowered or "facebook" in lowered or "linkedin" in lowered:
        channels.append("Social Media Marketing")
    if "referral" in lowered or "partner" in lowered:
        channels.append("Referral Programs")
    if "content" in lowered or "blog" in lowered:
        channels.append("Content Marketing")
    if "email" in lowered or "newsletter" in lowered:
        channels.append("Email Marketing")
    
    return channels or ["Website Traffic", "Word of Mouth", "Direct Marketing"]

def _analyze_pricing_strategy(text: str) -> str:
    """Analyze pricing strategy from content"""
    lowered = text.lower()
    
    if "free" in lowered and ("trial" in lowered or "demo" in lowered):
        return "Freemium/Trial-based pricing"
    elif "custom" in lowered or "quote" in lowered:
        return "Custom/Enterprise pricing"
    elif "subscription" in lowered or "monthly" in lowered:
        return "Subscription-based pricing"
    elif "package" in lowered or "tier" in lowered:
        return "Tiered pricing packages"
    else:
        return "Value-based pricing strategy"

def _assess_scalability(text: str, industry: str) -> str:
    """Assess business scalability potential"""
    lowered = text.lower()
    
    if "automation" in lowered or "platform" in lowered or "saas" in lowered:
        return "High scalability potential with digital infrastructure"
    elif "service" in lowered and industry != "Software / SaaS":
        return "Moderate scalability - service-based model may require scaling teams"
    elif "product" in lowered:
        return "Good scalability potential with product standardization"
    else:
        return "Scalability depends on operational efficiency improvements"

def _calculate_brand_presence(text: str, meta: Dict[str, Any]) -> int:
    """Calculate brand presence score (1-10)"""
    score = 5
    
    if meta.get("title") and len(meta.get("title", "")) > 10:
        score += 1
    if meta.get("description") and len(meta.get("description", "")) > 50:
        score += 1
    if meta.get("og"):
        score += 1
    if "brand" in text.lower() or "mission" in text.lower():
        score += 1
    if len(text) > 1000:
        score += 1
    
    return min(10, max(1, score))

def _assess_content_quality(text: str, heading_count: int) -> int:
    """Assess content quality score (1-10)"""
    score = 5
    
    score += min(2, heading_count // 2)  # Good structure
    score += min(2, len(text) // 1000)   # Content depth
    
    lowered = text.lower()
    if any(word in lowered for word in ["professional", "expert", "quality", "excellence"]):
        score += 1
    
    return min(10, max(1, score))

def _assess_user_experience(text: str, meta: Dict[str, Any]) -> int:
    """Assess user experience score (1-10)"""
    score = 5
    lowered = text.lower()
    
    if "contact" in lowered:
        score += 1
    if "about" in lowered:
        score += 1
    if meta.get("description"):
        score += 1
    if len(text) > 800:
        score += 1
    if "easy" in lowered or "simple" in lowered or "user-friendly" in lowered:
        score += 1
    
    return min(10, max(1, score))

def _find_social_proof(text: str) -> List[str]:
    """Find social proof indicators"""
    lowered = text.lower()
    proof = []
    
    if "testimonial" in lowered or "review" in lowered:
        proof.append("Customer testimonials")
    if "award" in lowered or "certified" in lowered:
        proof.append("Industry awards & certifications")
    if "client" in lowered or "customer" in lowered:
        proof.append("Client case studies")
    if "partner" in lowered:
        proof.append("Strategic partnerships")
    if any(num in text for num in ["100+", "1000+", "years"]):
        proof.append("Experience & scale metrics")
    
    return proof

def _generate_conversion_tips(text: str, industry: str) -> List[str]:
    """Generate conversion optimization tips"""
    lowered = text.lower()
    tips = []
    
    if "contact" not in lowered:
        tips.append("Add clear contact/CTA buttons")
    if "testimonial" not in lowered:
        tips.append("Include customer testimonials")
    if "pricing" not in lowered and "quote" not in lowered:
        tips.append("Display pricing or offer quotes")
    if "about" not in lowered:
        tips.append("Add compelling about section")
    
    # Industry-specific tips
    if industry == "E-commerce":
        tips.append("Optimize product pages with reviews")
    elif industry == "Software / SaaS":
        tips.append("Offer free trial or demo")
    
    return tips or ["Improve call-to-action placement", "Add trust signals"]

def _analyze_demographics(target_audience: str, text: str) -> str:
    """Analyze target demographics"""
    if "B2B" in target_audience:
        return "Business decision makers, C-level executives, department heads"
    elif "Families" in target_audience:
        return "Parents, caregivers, household decision makers"
    elif "Developers" in target_audience:
        return "Software developers, IT professionals, technical teams"
    else:
        return "Broad consumer market, age 25-55, tech-savvy users"

def _assess_website_performance(text: str, meta: Dict[str, Any]) -> int:
    """Assess website performance indicators (1-10)"""
    score = 5
    
    if meta.get("title"):
        score += 1
    if meta.get("description"):
        score += 1
    if meta.get("og"):
        score += 1
    if len(text) > 500:
        score += 1
    if "fast" in text.lower() or "quick" in text.lower():
        score += 1
    
    return min(10, max(1, score))

def _check_mobile_optimization(meta: Dict[str, Any]) -> str:
    """Check mobile optimization status"""
    viewport = meta.get("viewport", "")
    if "width=device-width" in str(viewport).lower():
        return "Mobile-responsive design detected"
    else:
        return "Mobile optimization needs verification"

def _assess_security(text: str) -> List[str]:
    """Assess security indicators"""
    lowered = text.lower()
    indicators = []
    
    if "secure" in lowered or "ssl" in lowered or "https" in lowered:
        indicators.append("SSL/HTTPS security")
    if "privacy" in lowered:
        indicators.append("Privacy policy present")
    if "gdpr" in lowered or "compliance" in lowered:
        indicators.append("Regulatory compliance mentioned")
    
    return indicators or ["Basic security measures recommended"]

def _identify_technical_debt(text: str) -> List[str]:
    """Identify potential technical debt areas"""
    lowered = text.lower()
    debt_areas = []
    
    if len(text) < 300:
        debt_areas.append("Limited content depth")
    if "update" in lowered or "maintenance" in lowered:
        debt_areas.append("Regular content updates needed")
    
    return debt_areas or ["Regular maintenance and updates recommended"]

def _find_integration_opportunities(text: str, industry: str) -> List[str]:
    """Find integration opportunities"""
    lowered = text.lower()
    opportunities = []
    
    if "crm" in lowered or "customer" in lowered:
        opportunities.append("CRM system integration")
    if "payment" in lowered or "billing" in lowered:
        opportunities.append("Payment gateway optimization")
    if "analytics" in lowered:
        opportunities.append("Advanced analytics platform")
    
    # Industry-specific
    if industry == "E-commerce":
        opportunities.append("Inventory management system")
    elif industry == "Software / SaaS":
        opportunities.append("API ecosystem development")
    
    return opportunities or ["Third-party tool integrations", "Automation platforms"]

def _generate_strategic_priorities(industry: str, text: str) -> List[str]:
    """Generate strategic priorities"""
    priorities = []
    lowered = text.lower()
    
    if "customer" in lowered:
        priorities.append("Enhance customer experience")
    if "growth" in lowered or "scale" in lowered:
        priorities.append("Scale operations efficiently")
    
    # Industry-specific priorities
    if industry == "Software / SaaS":
        priorities.extend(["Product development", "Market expansion"])
    elif industry == "Healthcare":
        priorities.extend(["Quality improvement", "Compliance management"])
    elif industry == "E-commerce":
        priorities.extend(["Inventory optimization", "Customer acquisition"])
    else:
        priorities.extend(["Market positioning", "Operational efficiency"])
    
    return priorities

def _identify_quick_wins(text: str, opportunities: List[str]) -> List[str]:
    """Identify quick wins"""
    quick_wins = []
    
    # From existing opportunities
    for opp in opportunities:
        if "seo" in opp.lower():
            quick_wins.append("Implement basic SEO improvements")
        elif "content" in opp.lower():
            quick_wins.append("Expand content marketing")
    
    # Additional quick wins
    if "contact" not in text.lower():
        quick_wins.append("Add clear contact information")
    
    return quick_wins or ["Optimize website conversion", "Enhance online presence"]

def _set_long_term_goals(industry: str, target_audience: str) -> List[str]:
    """Set long-term strategic goals"""
    goals = ["Achieve market leadership position", "Build sustainable competitive advantage"]
    
    if "B2B" in target_audience:
        goals.append("Develop enterprise-grade solutions")
    else:
        goals.append("Scale consumer market penetration")
    
    if industry == "Software / SaaS":
        goals.append("Build comprehensive platform ecosystem")
    elif industry == "Healthcare":
        goals.append("Establish centers of excellence")
    
    return goals

def _generate_investment_recommendations(industry: str, text: str) -> List[str]:
    """Generate investment recommendations"""
    recommendations = []
    lowered = text.lower()
    
    if "technology" in lowered or "digital" in lowered:
        recommendations.append("Technology infrastructure upgrade")
    if "team" in lowered or "hiring" in lowered:
        recommendations.append("Human capital investment")
    
    # Industry-specific
    if industry == "Software / SaaS":
        recommendations.extend(["R&D investment", "Cloud infrastructure"])
    elif industry == "E-commerce":
        recommendations.extend(["Inventory systems", "Customer acquisition"])
    else:
        recommendations.extend(["Marketing automation", "Process optimization"])
    
    return recommendations

def _calculate_overall_business_score(digital_score: int, brand_score: int, tech_score: int) -> int:
    """Calculate overall business score (1-100)"""
    weighted_score = (digital_score * 3 + brand_score * 3 + tech_score * 2) * 1.25
    return min(100, max(1, int(weighted_score)))

def _assess_growth_readiness(score: int) -> str:
    """Assess growth readiness based on overall score"""
    if score >= 80:
        return "High - Ready for aggressive growth"
    elif score >= 60:
        return "Medium - Good foundation for growth"
    elif score >= 40:
        return "Basic - Needs improvement before scaling"
    else:
        return "Low - Requires significant development"

def _identify_digital_transformation_needs(text: str, industry: str) -> List[str]:
    """Identify digital transformation needs"""
    lowered = text.lower()
    needs = []
    
    if "digital" not in lowered:
        needs.append("Digital strategy development")
    if "automation" not in lowered:
        needs.append("Process automation")
    if "data" not in lowered and "analytics" not in lowered:
        needs.append("Data analytics implementation")
    
    # Industry-specific needs
    if industry == "Healthcare" and "electronic" not in lowered:
        needs.append("Electronic health records")
    elif industry == "E-commerce" and "ai" not in lowered:
        needs.append("AI-powered recommendations")
    
    return needs or ["Cloud migration", "Digital workflow optimization"]


def select_provider() -> BaseProvider:
    for p in (OpenAIProvider(), OllamaProvider()):
        if p.available():
            return p
    return HeuristicProvider()


JSON_SCHEMA_HINT = {
    "industry": "string",
    "key_products": ["string"],
    "target_audience": "string",
    "website_strength": "string",
    "growth_opportunities": ["string"],
    "competitors": ["string"],
    "seo_summary": "string",
    "sentiment_summary": "string",
    "raw_findings": {"any": "object"},
    "report_text": "string",
}


def _build_prompt(text: str, meta: Dict[str, Any]) -> str:
    return (
        "Analyze the following website content and metadata. "
        "Return a concise JSON object with keys: industry, key_products (array), "
        "target_audience, website_strength, growth_opportunities (array), competitors (array), "
        "seo_summary, sentiment_summary, raw_findings (object), report_text.\n\n"
        f"Metadata: {json.dumps(meta)[:4000]}\n\n"
        f"Content (truncated): {text[:8000]}\n\n"
        "Respond ONLY with valid JSON, no code fences."
    )


def _parse_json_maybe(s: str) -> Optional[Dict[str, Any]]:
    s = s.strip()
    # Remove code fences if present
    s = re.sub(r"^```(?:json)?|```$", "", s, flags=re.IGNORECASE | re.MULTILINE)
    # Extract first JSON object
    m = re.search(r"\{[\s\S]*\}", s)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def analyze_text(text: str, meta: Optional[Dict[str, Any]] = None) -> InsightReport:
    meta = meta or {}
    provider = select_provider()

    if isinstance(provider, HeuristicProvider):
        return provider.analyze(text, meta)

    prompt = _build_prompt(text, meta)
    result = provider.generate(prompt)

    if not result.ok:
        # Fall back to heuristic on provider error
        return HeuristicProvider.analyze(text, meta)

    data = _parse_json_maybe(result.text)
    if not data:
        # Try lightweight recovery: ask heuristic
        return HeuristicProvider.analyze(text, meta)

    try:
        return InsightReport(**data)
    except Exception:
        return HeuristicProvider.analyze(text, meta)


def analyze_site(url: str) -> InsightReport:
    from .scraper import scrape_site

    content: SiteContent = scrape_site(url)
    return analyze_text(content.text, content.meta)
