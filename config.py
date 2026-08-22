"""
Job sources and personal job-search configuration.

Target:
    1. Kenya — Nairobi / anywhere in Kenya, including onsite/hybrid/remote.
    2. Remote worldwide — genuinely remote opportunities.

The notifier is intentionally focused on software development roles.
"""

SOURCES = [
    {
        "name": "MyJobMag Kenya",
        "type": "rss",
        "url": "https://www.myjobmag.co.ke/jobsxml.xml",
        "region": "kenya",
    },
    {
        "name": "MyJobMag Kenya - Categories",
        "type": "rss",
        "url": "https://www.myjobmag.co.ke/jobsxml_by_categories.xml",
        "region": "kenya",
    },
    {
        "name": "MyJobMag Kenya - Aggregate",
        "type": "rss",
        "url": "https://www.myjobmag.co.ke/aggregate_feed2.xml",
        "region": "kenya",
    },
    {
        "name": "RemoteOK",
        "type": "json_remoteok",
        "url": "https://remoteok.com/api",
        "region": "remote_worldwide",
    },
    {
        "name": "Remotive",
        "type": "rss",
        "url": "https://remotive.com/feed",
        "region": "remote_worldwide",
    },
]


# ---------------------------------------------------------------------------
# Software development roles
# ---------------------------------------------------------------------------

KEYWORDS = [
    # Core software engineering
    "software engineer",
    "software developer",
    "software development engineer",

    # Full stack
    "full stack engineer",
    "full-stack engineer",
    "fullstack engineer",
    "full stack developer",
    "full-stack developer",
    "fullstack developer",

    # Backend
    "backend engineer",
    "back-end engineer",
    "back end engineer",
    "backend developer",
    "back-end developer",
    "back end developer",

    # Frontend
    "frontend engineer",
    "front-end engineer",
    "front end engineer",
    "frontend developer",
    "front-end developer",
    "front end developer",

    # Web
    "web developer",
    "web engineer",

    # PHP / Laravel
    "laravel developer",
    "laravel engineer",
    "php developer",
    "php engineer",

    # React / TypeScript
    "react developer",
    "react engineer",
    "react.js developer",
    "react.js engineer",
    "typescript developer",
    "typescript engineer",

    # Node
    "node.js developer",
    "node.js engineer",
    "nodejs developer",
    "nodejs engineer",

    # General application development
    "application developer",
    "application engineer",

    # Engineering leadership
    "technical lead",
    "tech lead",
    "software engineering lead",
]


# ---------------------------------------------------------------------------
# Roles that are NOT the target
# ---------------------------------------------------------------------------

EXCLUDED_KEYWORDS = [
    # Business / sales
    "business developer",
    "business development",
    "sales development",
    "sales developer",
    "account manager",
    "account executive",

    # Product / project
    "product manager",
    "project manager",
    "program manager",
    "product owner",

    # Support
    "customer success",
    "customer support",
    "technical support",
    "it support",
    "help desk",
    "helpdesk",

    # Developer advocacy / marketing
    "developer relations",
    "developer advocate",
    "developer marketing",

    # DevOps / infrastructure / SRE
    "devops",
    "devops engineer",
    "site reliability engineer",
    "sre engineer",
    "platform reliability",

    # QA / testing
    "qa engineer",
    "quality assurance",
    "test engineer",
    "software development engineer in test",
    "sdet",

    # Data / ML
    "data engineer",
    "data scientist",
    "machine learning engineer",
    "ml engineer",
    "research scientist",

    # Mobile
    "mobile developer",
    "mobile engineer",
    "ios developer",
    "android developer",
    "flutter developer",
    "react native developer",

    # Embedded / hardware / games
    "embedded engineer",
    "embedded developer",
    "hardware engineer",
    "game developer",

    # Junior / internship
    "intern",
    "internship",
    "graduate trainee",
]


# ---------------------------------------------------------------------------
# Kenya
# ---------------------------------------------------------------------------

KENYA_KEYWORDS = [
    "kenya",
    "nairobi",
    "mombasa",
    "kisumu",
    "nakuru",
    "kiambu",
    "eldoret",
    "machakos",
    "thika",
    "kenyan",
]


# ---------------------------------------------------------------------------
# Remote indicators
# ---------------------------------------------------------------------------

REMOTE_KEYWORDS = [
    "remote",
    "work from home",
    "work from anywhere",
    "anywhere",
    "distributed",
]


def active_sources():
    return [
        source
        for source in SOURCES
        if source["url"]
        and "PASTE_" not in source["url"]
    ]