from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass
class FollowerRange:
    minimum: Optional[int] = None
    maximum: Optional[int] = None


@dataclass
class Job:
    job_id: str
    client_name: str
    niche: str
    keywords: List[str]
    location: Optional[str] = None
    language: Optional[str] = None
    goals: Optional[str] = None
    exclude_accounts: List[str] = field(default_factory=list)
    follower_range: FollowerRange = field(default_factory=FollowerRange)
    min_er_percent: Optional[float] = None
    package: str = "starter"
    notes: Optional[str] = None
    seed_handles: List[str] = field(default_factory=list)
    posts_sample: Optional[int] = None


@dataclass
class CandidateCreator:
    username: str
    user_id: Optional[str] = None
    source_keyword: Optional[str] = None


@dataclass
class CreatorMetrics:
    followers: int
    following: int
    avg_likes: float
    avg_comments: float
    er_percent: float
    posts_sampled: int
    last_post_days_ago: Optional[int] = None
    posts_last_30d: Optional[int] = None


@dataclass
class CreatorRecord:
    username: str
    profile_url: Optional[str]
    full_name: Optional[str]
    followers: int
    following: int
    posts: Optional[int]
    avg_likes: float
    avg_comments: float
    er_percent: float
    last_post_days_ago: Optional[int]
    posts_last_30d: Optional[int]
    quality_flag: str
    reason_notes: str
    contact_email: Optional[str]
    external_url: Optional[str]
    source_keyword: Optional[str]


@dataclass
class RequestCost:
    endpoint: str
    units: int


@dataclass
class RunStats:
    job_id: str
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_request_units: int = 0
    cost_by_endpoint: Dict[str, int] = field(default_factory=dict)
    cache_hits: int = 0
    cache_misses: int = 0

    def record_cost(self, endpoint: str, units: int) -> None:
        self.total_request_units += units
        self.cost_by_endpoint[endpoint] = self.cost_by_endpoint.get(endpoint, 0) + units

