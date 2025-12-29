"""Fetch Reddit threads and comments."""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import praw
from praw.models import MoreComments

from ingestion.reddit_client import RedditClient
from ingestion.normalize import normalize_text


def fetch_thread(
    url: str,
    comment_limit: Optional[int] = None,
    include_removed: bool = False,
) -> Dict[str, Any]:
    """Fetch a Reddit thread with all comments.

    Args:
        url: Reddit thread URL
        comment_limit: Maximum comments to fetch (None = all)
        include_removed: Include deleted/removed comments

    Returns:
        Structured thread data with comments
    """
    client = RedditClient()
    submission = client.get_submission_from_url(url)

    # Expand all comments
    submission.comments.replace_more(limit=None if comment_limit is None else 0)

    # Extract thread metadata
    thread_data = {
        "thread_id": submission.id,
        "title": submission.title,
        "subreddit": str(submission.subreddit),
        "author": str(submission.author) if submission.author else "[deleted]",
        "created_utc": int(submission.created_utc),
        "score": submission.score,
        "num_comments": submission.num_comments,
        "url": submission.url,
        "selftext": submission.selftext,
        "comments": [],
    }

    # Extract comments
    comments = []
    for comment in submission.comments.list():
        if isinstance(comment, MoreComments):
            continue

        # Skip deleted/removed if not requested
        if not include_removed:
            if comment.author is None or comment.body in ["[deleted]", "[removed]"]:
                continue

        comment_data = {
            "id": comment.id,
            "author": str(comment.author) if comment.author else "[deleted]",
            "text": comment.body,
            "text_normalized": normalize_text(comment.body),
            "created_utc": int(comment.created_utc),
            "score": comment.score,
            "parent_id": comment.parent_id,
            "is_submitter": comment.is_submitter,
            "edited": bool(comment.edited),
        }
        comments.append(comment_data)

        if comment_limit and len(comments) >= comment_limit:
            break

    thread_data["comments"] = comments
    thread_data["comments_analyzed"] = len(comments)

    return thread_data


def fetch_subreddit_threads(
    subreddit_name: str,
    time_filter: str = "day",
    limit: int = 10,
    sort: str = "hot",
) -> List[Dict[str, Any]]:
    """Fetch multiple threads from a subreddit.

    Args:
        subreddit_name: Subreddit name (without r/)
        time_filter: Time filter (hour, day, week, month, year, all)
        limit: Number of threads to fetch
        sort: Sort method (hot, new, top, rising, controversial)

    Returns:
        List of thread data dictionaries
    """
    client = RedditClient()
    subreddit = client.get_subreddit(subreddit_name)

    # Get submissions based on sort method
    if sort == "hot":
        submissions = subreddit.hot(limit=limit)
    elif sort == "new":
        submissions = subreddit.new(limit=limit)
    elif sort == "top":
        submissions = subreddit.top(time_filter=time_filter, limit=limit)
    elif sort == "rising":
        submissions = subreddit.rising(limit=limit)
    elif sort == "controversial":
        submissions = subreddit.controversial(time_filter=time_filter, limit=limit)
    else:
        raise ValueError(f"Unknown sort method: {sort}")

    threads = []
    for submission in submissions:
        thread_data = fetch_thread(f"https://reddit.com{submission.permalink}")
        threads.append(thread_data)

    return threads


def fetch_subreddit_window(
    subreddit_name: str,
    hours: int = 24,
    comment_threshold: int = 20,
) -> List[Dict[str, Any]]:
    """Fetch threads from a subreddit within a time window.

    Args:
        subreddit_name: Subreddit name (without r/)
        hours: Hours to look back
        comment_threshold: Minimum comments required

    Returns:
        List of thread data for threads with sufficient activity
    """
    client = RedditClient()
    subreddit = client.get_subreddit(subreddit_name)

    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    cutoff_timestamp = int(cutoff_time.timestamp())

    threads = []
    for submission in subreddit.new(limit=100):
        # Check if within time window
        if submission.created_utc < cutoff_timestamp:
            break

        # Check if meets comment threshold
        if submission.num_comments < comment_threshold:
            continue

        thread_data = fetch_thread(f"https://reddit.com{submission.permalink}")
        threads.append(thread_data)

    return threads


def get_user_comment_history(
    username: str,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Fetch a user's comment history.

    Args:
        username: Reddit username (without u/)
        limit: Maximum comments to fetch

    Returns:
        List of comment data
    """
    client = RedditClient()
    user = client.get_user(username)

    comments = []
    for comment in user.comments.new(limit=limit):
        comment_data = {
            "id": comment.id,
            "subreddit": str(comment.subreddit),
            "text": comment.body,
            "text_normalized": normalize_text(comment.body),
            "created_utc": int(comment.created_utc),
            "score": comment.score,
            "submission_id": comment.submission.id,
        }
        comments.append(comment_data)

    return comments


def extract_submission_id(url: str) -> str:
    """Extract submission ID from Reddit URL.

    Args:
        url: Reddit URL

    Returns:
        Submission ID
    """
    # Handle different URL formats
    if "/comments/" in url:
        parts = url.split("/comments/")[1].split("/")
        return parts[0]
    else:
        raise ValueError(f"Could not extract submission ID from URL: {url}")
