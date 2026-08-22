"""
LinkedIn search links.

We do not scrape or authenticate against LinkedIn.
The daily email contains targeted LinkedIn searches that can
be opened manually.
"""

from urllib.parse import quote


def linkedin_url(keywords: str, location: str | None = None) -> str:
    url = (
        "https://www.linkedin.com/jobs/search/?keywords="
        + quote(keywords)
    )

    if location:
        url += "&location=" + quote(location)

    return url


def linkedin_remote_url(keywords: str) -> str:
    """
    LinkedIn remote-work search.

    f_WT=2 is LinkedIn's remote-work filter.
    It does NOT guarantee worldwide eligibility, so the email
    labels these simply as Remote.
    """

    return (
        "https://www.linkedin.com/jobs/search/?keywords="
        + quote(keywords)
        + "&f_WT=2"
    )


LINKEDIN_SEARCHES = [
    # ------------------------------------------------------------------
    # Kenya
    # ------------------------------------------------------------------

    {
        "name": "Senior Software Engineer — Kenya",
        "location": "Kenya",
        "url": linkedin_url(
            "Senior Software Engineer",
            "Kenya",
        ),
    },
    {
        "name": "Software Developer — Kenya",
        "location": "Kenya",
        "url": linkedin_url(
            "Software Developer",
            "Kenya",
        ),
    },
    {
        "name": "Full Stack Developer — Kenya",
        "location": "Kenya",
        "url": linkedin_url(
            "Full Stack Developer",
            "Kenya",
        ),
    },
    {
        "name": "Backend Developer — Kenya",
        "location": "Kenya",
        "url": linkedin_url(
            "Backend Developer",
            "Kenya",
        ),
    },
    {
        "name": "PHP Laravel Developer — Kenya",
        "location": "Kenya",
        "url": linkedin_url(
            "PHP Laravel Developer",
            "Kenya",
        ),
    },
    {
        "name": "React TypeScript Developer — Kenya",
        "location": "Kenya",
        "url": linkedin_url(
            "React TypeScript Developer",
            "Kenya",
        ),
    },

    # ------------------------------------------------------------------
    # Remote
    # ------------------------------------------------------------------

    {
        "name": "Senior Software Engineer — Remote",
        "location": "Worldwide",
        "url": linkedin_remote_url(
            "Senior Software Engineer",
        ),
    },
    {
        "name": "Software Developer — Remote",
        "location": "Worldwide",
        "url": linkedin_remote_url(
            "Software Developer",
        ),
    },
    {
        "name": "Full Stack Developer — Remote",
        "location": "Worldwide",
        "url": linkedin_remote_url(
            "Full Stack Developer",
        ),
    },
    {
        "name": "Backend Developer — Remote",
        "location": "Worldwide",
        "url": linkedin_remote_url(
            "Backend Developer",
        ),
    },
    {
        "name": "Laravel PHP Developer — Remote",
        "location": "Worldwide",
        "url": linkedin_remote_url(
            "Laravel PHP Developer",
        ),
    },
]


def get_linkedin_searches() -> list[dict]:
    return LINKEDIN_SEARCHES