from datetime import datetime
from typing import List

from ..hiker.client import HikerAPIClient
from ..types import CandidateCreator, CreatorMetrics, CreatorRecord, Job
from .metrics import compute_post_activity, compute_profile_metrics
from .scoring import score_creator


def enrich_candidates(
    candidates: List[CandidateCreator],
    job: Job,
    client: HikerAPIClient,
    posts_sample: int,
) -> List[CreatorRecord]:
    records: List[CreatorRecord] = []

    for candidate in candidates:
        try:
            profile = client.fetch_profile(candidate.username)
            posts = client.fetch_recent_posts(candidate.username, limit=posts_sample)
        except Exception as exc:  # noqa: BLE001
            records.append(
                CreatorRecord(
                    username=candidate.username,
                    profile_url=f"https://www.instagram.com/{candidate.username}/",
                    full_name=None,
                    followers=0,
                    following=0,
                    posts=None,
                    avg_likes=0.0,
                    avg_comments=0.0,
                    er_percent=0.0,
                    last_post_days_ago=None,
                    posts_last_30d=None,
                    quality_flag="Avoid",
                    reason_notes=f"Fetch failed: {exc}",
                    contact_email=None,
                    external_url=None,
                    source_keyword=candidate.source_keyword,
                )
            )
            continue

        metrics_dict = compute_profile_metrics(profile, posts)
        last_post_days_ago, posts_last_30d = compute_post_activity(posts)

        metrics = CreatorMetrics(
            followers=metrics_dict["followers"],
            following=metrics_dict["following"],
            avg_likes=metrics_dict["avg_likes"],
            avg_comments=metrics_dict["avg_comments"],
            er_percent=metrics_dict["er_percent"],
            posts_sampled=metrics_dict["posts_sampled"],
            last_post_days_ago=last_post_days_ago,
            posts_last_30d=posts_last_30d,
        )

        flag, note = score_creator(metrics, posts_last_30d or 0, last_post_days_ago or 0, job)

        profile_url = f"https://www.instagram.com/{candidate.username}/"
        record = CreatorRecord(
            username=candidate.username,
            profile_url=profile_url,
            full_name=profile.get("full_name") or profile.get("name"),
            followers=metrics.followers,
            following=metrics.following,
            posts=profile.get("posts") or profile.get("media_count") or len(posts),
            avg_likes=metrics.avg_likes,
            avg_comments=metrics.avg_comments,
            er_percent=metrics.er_percent,
            last_post_days_ago=metrics.last_post_days_ago,
            posts_last_30d=metrics.posts_last_30d,
            quality_flag=flag,
            reason_notes=note,
            contact_email=profile.get("email"),
            external_url=profile.get("external_url"),
            source_keyword=candidate.source_keyword,
        )

        records.append(record)

    return records

