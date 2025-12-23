from typing import List

from ..types import CandidateCreator, Job


def discover_candidates(job: Job) -> List[CandidateCreator]:
    """
    Placeholder discovery step.

    For now, we rely on explicit seed handles from the job brief to avoid
    undefined API calls. Future iterations will search keywords/hashtags via
    HikerAPI to build this list automatically.
    """

    candidates: List[CandidateCreator] = []
    for handle in job.seed_handles:
        candidates.append(CandidateCreator(username=handle))
    return candidates

