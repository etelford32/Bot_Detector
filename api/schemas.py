"""Pydantic schemas for API requests and responses."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, HttpUrl, Field


class AnalyzeThreadRequest(BaseModel):
    """Request to analyze a single thread."""

    url: str = Field(..., description="Reddit thread URL")
    use_cache: bool = Field(True, description="Use embedding cache")


class AnalyzeSubredditRequest(BaseModel):
    """Request to analyze a subreddit."""

    subreddit: str = Field(..., description="Subreddit name (without r/)")
    time_filter: str = Field("day", description="Time filter (hour, day, week, month, year)")
    limit: int = Field(10, description="Number of threads to analyze", ge=1, le=50)
    sort: str = Field("hot", description="Sort method (hot, new, top, rising)")


class ThreadInfo(BaseModel):
    """Thread information."""

    id: str
    title: str
    subreddit: str
    url: str
    score: int
    num_comments: int


class AnalysisResult(BaseModel):
    """Analysis result for a thread."""

    score: float = Field(..., description="Synthetic consensus score (0-100)")
    interpretation: str = Field(..., description="Score interpretation")
    confidence: str = Field(..., description="Confidence level")
    n_analyzed: int = Field(..., description="Number of comments analyzed")


class ComponentScores(BaseModel):
    """Component scores breakdown."""

    semantic_score: float
    temporal_score: float
    network_score: float


class AnalyzeThreadResponse(BaseModel):
    """Response for thread analysis."""

    thread: ThreadInfo
    analysis: AnalysisResult
    signals: ComponentScores
    key_findings: List[str]
    rationale: str


class AnalyzeSubredditResponse(BaseModel):
    """Response for subreddit analysis."""

    subreddit: str
    analyzed_threads: int
    results: List[Dict[str, Any]]
    summary: Dict[str, Any]


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    models_loaded: bool


class ErrorResponse(BaseModel):
    """Error response."""

    error: str
    detail: Optional[str] = None
