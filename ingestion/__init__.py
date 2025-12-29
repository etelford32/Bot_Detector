"""Reddit data ingestion module."""

from ingestion.reddit_client import RedditClient
from ingestion.thread_fetcher import (
    fetch_thread,
    fetch_subreddit_threads,
    fetch_subreddit_window,
    get_user_comment_history,
    extract_submission_id,
)
from ingestion.normalize import (
    normalize_text,
    is_trivial_comment,
    get_text_stats,
)

__all__ = [
    "RedditClient",
    "fetch_thread",
    "fetch_subreddit_threads",
    "fetch_subreddit_window",
    "get_user_comment_history",
    "extract_submission_id",
    "normalize_text",
    "is_trivial_comment",
    "get_text_stats",
]
