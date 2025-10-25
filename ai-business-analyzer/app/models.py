from __future__ import annotations

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field


class AnalysisRequest(BaseModel):
    url: Optional[str] = Field(default=None, description="Target website URL to analyze")
    description: Optional[str] = Field(default=None, description="Free-text business description if no URL")


class SiteContent(BaseModel):
    url: Optional[str]
    text: str
    meta: Dict[str, Any]
    links: List[str] = []


class BusinessInsights(BaseModel):
    """Comprehensive business analytics and insights"""
    market_positioning: Optional[str] = None
    revenue_streams: List[str] = []
    competitive_advantages: List[str] = []
    risk_factors: List[str] = []
    digital_maturity_score: Optional[int] = Field(default=None, ge=1, le=10)
    customer_acquisition_channels: List[str] = []
    pricing_strategy: Optional[str] = None
    scalability_assessment: Optional[str] = None


class MarketingAnalytics(BaseModel):
    """Marketing and customer engagement metrics"""
    brand_presence_score: Optional[int] = Field(default=None, ge=1, le=10)
    content_quality_score: Optional[int] = Field(default=None, ge=1, le=10)
    user_experience_score: Optional[int] = Field(default=None, ge=1, le=10)
    social_proof_indicators: List[str] = []
    conversion_optimization_tips: List[str] = []
    target_demographics: Optional[str] = None


class TechnicalAnalytics(BaseModel):
    """Technical and digital performance insights"""
    website_performance_score: Optional[int] = Field(default=None, ge=1, le=10)
    mobile_optimization: Optional[str] = None
    security_indicators: List[str] = []
    technical_debt_areas: List[str] = []
    integration_opportunities: List[str] = []


class InsightReport(BaseModel):
    # Original fields
    industry: Optional[str] = None
    key_products: List[str] = []
    target_audience: Optional[str] = None
    website_strength: Optional[str] = None
    growth_opportunities: List[str] = []
    competitors: List[str] = []
    seo_summary: Optional[str] = None
    sentiment_summary: Optional[str] = None
    raw_findings: Dict[str, object] = {}
    report_text: Optional[str] = None
    
    # Enhanced business analytics
    business_insights: Optional[BusinessInsights] = None
    marketing_analytics: Optional[MarketingAnalytics] = None
    technical_analytics: Optional[TechnicalAnalytics] = None
    
    # Strategic recommendations
    strategic_priorities: List[str] = []
    quick_wins: List[str] = []
    long_term_goals: List[str] = []
    investment_recommendations: List[str] = []
    
    # Performance metrics
    overall_business_score: Optional[int] = Field(default=None, ge=1, le=100)
    readiness_for_growth: Optional[str] = None
    digital_transformation_needs: List[str] = []


__all__ = [
    "AnalysisRequest",
    "SiteContent",
    "InsightReport",
    "BusinessInsights",
    "MarketingAnalytics", 
    "TechnicalAnalytics",
]
