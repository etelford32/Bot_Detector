"""Reddit API client wrapper using PRAW."""

import os
from typing import Optional
import praw
from dotenv import load_dotenv

load_dotenv()


class RedditClient:
    """Wrapper for Reddit API access using PRAW."""

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        user_agent: Optional[str] = None,
    ):
        """Initialize Reddit client.

        Args:
            client_id: Reddit app client ID (defaults to env var)
            client_secret: Reddit app client secret (defaults to env var)
            user_agent: User agent string (defaults to env var)
        """
        self.client_id = client_id or os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = user_agent or os.getenv(
            "REDDIT_USER_AGENT", "ConsensusWatch/0.1.0"
        )

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Reddit API credentials not found. "
                "Set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables."
            )

        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )

    def get_submission(self, submission_id: str) -> praw.models.Submission:
        """Fetch a submission by ID.

        Args:
            submission_id: Reddit submission ID

        Returns:
            PRAW Submission object
        """
        return self.reddit.submission(id=submission_id)

    def get_submission_from_url(self, url: str) -> praw.models.Submission:
        """Fetch a submission from URL.

        Args:
            url: Full Reddit submission URL

        Returns:
            PRAW Submission object
        """
        return self.reddit.submission(url=url)

    def get_subreddit(self, subreddit_name: str) -> praw.models.Subreddit:
        """Fetch a subreddit by name.

        Args:
            subreddit_name: Subreddit name (without r/)

        Returns:
            PRAW Subreddit object
        """
        return self.reddit.subreddit(subreddit_name)

    def get_user(self, username: str) -> praw.models.Redditor:
        """Fetch a user by username.

        Args:
            username: Reddit username (without u/)

        Returns:
            PRAW Redditor object
        """
        return self.reddit.redditor(username)

    @property
    def is_authenticated(self) -> bool:
        """Check if client is authenticated."""
        try:
            # Try to access user (will fail if not authenticated)
            _ = self.reddit.user.me()
            return True
        except Exception:
            return False
