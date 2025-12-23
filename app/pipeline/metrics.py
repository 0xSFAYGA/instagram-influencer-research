from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional, Tuple


def safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def engagement_rate_percent(
    total_likes: float, total_comments: float, follower_count: float
) -> float:
    """Average engagement per follower for the sampled posts, as a percent."""
    return safe_divide(total_likes + total_comments, follower_count) * 100


def average_interactions(posts: Iterable[Dict]) -> Dict[str, float]:
    likes = [post.get("likes", 0) or 0 for post in posts]
    comments = [post.get("comments", 0) or 0 for post in posts]
    count = max(len(likes), 1)
    return {
        "avg_likes": sum(likes) / count,
        "avg_comments": sum(comments) / count,
    }


def parse_posted_at(posted_at: Optional[str]) -> Optional[datetime]:
    if not posted_at:
        return None
    try:
        return datetime.fromisoformat(posted_at.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None


def compute_post_activity(posts: List[Dict]) -> Tuple[Optional[int], Optional[int]]:
    now = datetime.utcnow()
    dates = [parse_posted_at(post.get("posted_at")) for post in posts]
    dates = [d for d in dates if d]

    if not dates:
        return None, None

    last_post_days_ago = (now - max(dates)).days

    window_start = now - timedelta(days=30)
    posts_last_30d = sum(1 for d in dates if d >= window_start)

    return last_post_days_ago, posts_last_30d


def compute_profile_metrics(profile: Dict, posts: List[Dict]) -> Dict[str, float]:
    follower_count = profile.get("followers", 0) or 0
    likes = sum(post.get("likes", 0) or 0 for post in posts)
    comments = sum(post.get("comments", 0) or 0 for post in posts)

    averages = average_interactions(posts)

    return {
        "followers": follower_count,
        "following": profile.get("following", 0) or 0,
        "avg_likes": averages["avg_likes"],
        "avg_comments": averages["avg_comments"],
        "er_percent": engagement_rate_percent(likes, comments, follower_count),
        "posts_sampled": len(posts),
    }

