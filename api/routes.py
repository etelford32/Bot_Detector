"""API routes for bot detection."""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from api.schemas import (
    AnalyzeThreadRequest,
    AnalyzeThreadResponse,
    AnalyzeSubredditRequest,
    AnalyzeSubredditResponse,
    HealthResponse,
)
from ingestion.thread_fetcher import fetch_thread, fetch_subreddit_threads
from analysis.consensus_score import calculate_consensus_score
from explainability.rationale import generate_rationale
from explainability.summaries import generate_json_summary

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        models_loaded=True,
    )


@router.post("/analyze", response_model=AnalyzeThreadResponse)
async def analyze_thread(request: AnalyzeThreadRequest) -> AnalyzeThreadResponse:
    """Analyze a Reddit thread for synthetic consensus.

    Args:
        request: Analysis request with thread URL

    Returns:
        Analysis results with score and explanation

    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Fetch thread data
        thread_data = fetch_thread(request.url)

        # Calculate consensus score
        score, metrics = calculate_consensus_score(thread_data, request.use_cache)

        # Generate rationale
        rationale = generate_rationale(score, metrics)

        # Generate JSON summary
        summary = generate_json_summary(thread_data, score, metrics)

        # Build response
        return AnalyzeThreadResponse(
            thread=summary["thread"],
            analysis=summary["analysis"],
            signals=summary["signals"],
            key_findings=summary["key_findings"],
            rationale=rationale,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/subreddit", response_model=AnalyzeSubredditResponse)
async def analyze_subreddit(
    request: AnalyzeSubredditRequest,
) -> AnalyzeSubredditResponse:
    """Analyze multiple threads from a subreddit.

    Args:
        request: Subreddit analysis request

    Returns:
        Analysis results for multiple threads

    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Fetch threads
        threads = fetch_subreddit_threads(
            request.subreddit,
            time_filter=request.time_filter,
            limit=request.limit,
            sort=request.sort,
        )

        # Analyze each thread
        results = []
        scores = []

        for thread_data in threads:
            try:
                score, metrics = calculate_consensus_score(thread_data)
                summary = generate_json_summary(thread_data, score, metrics)
                results.append(summary)
                scores.append(score)
            except Exception as e:
                # Skip failed threads
                continue

        # Calculate summary statistics
        summary_stats = {
            "avg_score": sum(scores) / len(scores) if scores else 0.0,
            "max_score": max(scores) if scores else 0.0,
            "min_score": min(scores) if scores else 0.0,
            "high_risk_threads": sum(1 for s in scores if s >= 75),
            "medium_risk_threads": sum(1 for s in scores if 50 <= s < 75),
            "low_risk_threads": sum(1 for s in scores if s < 50),
        }

        return AnalyzeSubredditResponse(
            subreddit=request.subreddit,
            analyzed_threads=len(results),
            results=results,
            summary=summary_stats,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "service": "ConsensusWatch API",
        "version": "0.1.0",
        "docs": "/docs",
    }
