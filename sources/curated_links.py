"""
Manual-check links for job boards with no public RSS/JSON feed.

MyGreenhouse (my.greenhouse.io) and the 80,000 Hours job board were both
checked (2026-10) and neither exposes a documented, public way to poll
listings programmatically — unlike individual Greenhouse/Ashby/Workable
company boards, which are polled directly in config.py. Rather than
scraping their HTML (fragile, against most boards' terms of use), these
are surfaced as direct search links, the same way LinkedIn is handled.
"""

CURATED_LINKS = [
    {
        "name": "MyGreenhouse — cross-company search",
        "url": "https://my.greenhouse.io/jobs/search",
    },
    {
        "name": "80,000 Hours Job Board",
        "url": "https://jobs.80000hours.org/",
    },
]


def get_curated_links() -> list[dict]:
    return CURATED_LINKS
