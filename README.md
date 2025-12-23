# Instagram Influencer Research

Decision-ready Instagram influencer research pipeline built around HikerAPI.

## Quick start
1. Install deps: `pip install -r requirements.txt`
2. Create `.env` (see `.env.example` for keys).
3. Add a job brief at `inputs/job.json` (see sample below).
4. Run: `python -m app run inputs/job.json`

Outputs land in `data/jobs/<job_id>/` as `output.csv`, `output.xlsx`, `summary.md`, `run_log.jsonl` (and `action_plan.md` for Advanced).

## Job brief (minimum)
```json
{
  "job_id": "ACME-2025-12-20-001",
  "client_name": "ACME",
  "niche": "skincare",
  "keywords": ["acne", "retinol", "spf"],
  "location": "US",
  "language": "en",
  "goals": "conversions",
  "exclude_accounts": ["competitor1"],
  "follower_range": {"min": 5000, "max": 250000},
  "min_er_percent": 1.5,
  "package": "standard",
  "notes": "Prefer micro creators and consistent posting.",
  "seed_handles": ["example_creator1", "example_creator2"]
}
```

Notes:
- Discovery currently relies on `seed_handles`; keyword/hashtag discovery will be added next.
- `posts_sample` can override the default number of posts sampled per creator (otherwise defaults to `DEFAULT_POSTS_SAMPLE`).
