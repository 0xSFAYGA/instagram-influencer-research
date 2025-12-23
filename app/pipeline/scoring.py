from typing import List, Tuple

from ..types import CreatorMetrics, Job


def score_creator(metrics: CreatorMetrics, posts_last_30d: int, last_post_days_ago: int, job: Job) -> Tuple[str, str]:
    reasons: List[str] = []

    min_er = job.min_er_percent or 1.0
    follower_min = job.follower_range.minimum
    follower_max = job.follower_range.maximum

    if follower_min is not None and metrics.followers < follower_min:
        reasons.append("Below min follower range")
    if follower_max is not None and metrics.followers > follower_max:
        reasons.append("Above max follower range")

    if metrics.er_percent < min_er:
        reasons.append(f"ER below {min_er}% target")

    if posts_last_30d == 0:
        reasons.append("No posts in last 30 days")
    elif posts_last_30d is not None and posts_last_30d < 2:
        reasons.append("Low recent posting")

    if last_post_days_ago is not None and last_post_days_ago > 90:
        reasons.append("Inactive >90 days")

    flag = "Recommended"
    if reasons:
        flag = "Review"
    if metrics.er_percent < 0.5 or posts_last_30d == 0 or (
        last_post_days_ago is not None and last_post_days_ago > 120
    ):
        flag = "Avoid"

    note = " • ".join(reasons) if reasons else "Fits brief"
    return flag, note

