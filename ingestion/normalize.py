"""Text normalization utilities for Reddit comments."""

import re
from typing import Optional


def normalize_text(text: str, preserve_case: bool = False) -> str:
    """Normalize Reddit comment text.

    Args:
        text: Raw comment text
        preserve_case: Keep original casing (default: lowercase)

    Returns:
        Normalized text
    """
    if not text or text in ["[deleted]", "[removed]"]:
        return ""

    # Remove URLs
    text = remove_urls(text)

    # Remove Reddit markdown formatting
    text = remove_markdown(text)

    # Remove Reddit username mentions
    text = remove_mentions(text)

    # Remove subreddit references
    text = remove_subreddit_refs(text)

    # Normalize whitespace
    text = normalize_whitespace(text)

    # Convert to lowercase unless preserving case
    if not preserve_case:
        text = text.lower()

    return text.strip()


def remove_urls(text: str) -> str:
    """Remove URLs from text.

    Args:
        text: Input text

    Returns:
        Text with URLs removed
    """
    # Match http/https URLs
    text = re.sub(r'https?://\S+', '', text)

    # Match www URLs
    text = re.sub(r'www\.\S+', '', text)

    return text


def remove_markdown(text: str) -> str:
    """Remove Reddit markdown formatting.

    Args:
        text: Input text with markdown

    Returns:
        Text without markdown
    """
    # Remove bold/italic markers
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # **bold**
    text = re.sub(r'\*(.+?)\*', r'\1', text)      # *italic*
    text = re.sub(r'__(.+?)__', r'\1', text)      # __bold__
    text = re.sub(r'_(.+?)_', r'\1', text)        # _italic_

    # Remove strikethrough
    text = re.sub(r'~~(.+?)~~', r'\1', text)

    # Remove code blocks
    text = re.sub(r'`(.+?)`', r'\1', text)

    # Remove quotes
    text = re.sub(r'^>\s*', '', text, flags=re.MULTILINE)

    # Remove headers
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)

    # Remove list markers
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

    return text


def remove_mentions(text: str) -> str:
    """Remove Reddit username mentions.

    Args:
        text: Input text

    Returns:
        Text without mentions
    """
    # Remove u/username
    text = re.sub(r'\bu/\w+', '', text)

    # Remove /u/username
    text = re.sub(r'\b/u/\w+', '', text)

    return text


def remove_subreddit_refs(text: str) -> str:
    """Remove subreddit references.

    Args:
        text: Input text

    Returns:
        Text without subreddit references
    """
    # Remove r/subreddit
    text = re.sub(r'\br/\w+', '', text)

    # Remove /r/subreddit
    text = re.sub(r'\b/r/\w+', '', text)

    return text


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text.

    Args:
        text: Input text

    Returns:
        Text with normalized whitespace
    """
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)

    # Remove leading/trailing whitespace
    text = text.strip()

    return text


def is_trivial_comment(text: str, min_length: int = 5) -> bool:
    """Check if comment is trivial (too short, low-content).

    Args:
        text: Normalized comment text
        min_length: Minimum character length

    Returns:
        True if comment is trivial
    """
    if not text or len(text) < min_length:
        return True

    # Check for common trivial comments
    trivial_patterns = [
        r'^this\.?$',
        r'^lol\.?$',
        r'^lmao\.?$',
        r'^same\.?$',
        r'^agree[d]?\.?$',
        r'^yes\.?$',
        r'^no\.?$',
        r'^yeah\.?$',
        r'^nope\.?$',
        r'^\+1\.?$',
        r'^upvoted?\.?$',
        r'^came here to say this\.?$',
    ]

    text_lower = text.lower().strip()
    for pattern in trivial_patterns:
        if re.match(pattern, text_lower):
            return True

    return False


def extract_quoted_text(text: str) -> Optional[str]:
    """Extract quoted text from comment (if replying to someone).

    Args:
        text: Comment text

    Returns:
        Quoted portion, if found
    """
    # Match > quote blocks
    quotes = re.findall(r'^>\s*(.+)$', text, flags=re.MULTILINE)

    if quotes:
        return ' '.join(quotes)

    return None


def get_text_stats(text: str) -> dict:
    """Get basic statistics about text.

    Args:
        text: Input text

    Returns:
        Dictionary of text statistics
    """
    words = text.split()

    return {
        "char_count": len(text),
        "word_count": len(words),
        "avg_word_length": sum(len(w) for w in words) / len(words) if words else 0,
        "unique_words": len(set(words)),
        "vocabulary_ratio": len(set(words)) / len(words) if words else 0,
    }
