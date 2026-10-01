"""
Job sources and personal job-search configuration.

Target:
    1. Kenya — Nairobi / anywhere in Kenya, including onsite/hybrid/remote.
    2. Remote worldwide — genuinely remote opportunities.

The notifier is intentionally focused on software development roles.
"""

SOURCES = [
    # ============================================================
    # KENYA
    # ============================================================

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

    # Add these only after confirming the current feed/search URL.
    {
        "name": "BrighterMonday Kenya",
        "type": "rss",
        "url": "",
        "region": "kenya",
    },

    {
        "name": "Fuzu Kenya",
        "type": "rss",
        "url": "",
        "region": "kenya",
    },

    {
        "name": "Career Point Kenya",
        "type": "rss",
        "url": "",
        "region": "kenya",
    },

    {
        "name": "Corporate Staffing Kenya",
        "type": "rss",
        "url": "",
        "region": "kenya",
    },


    # ============================================================
    # REMOTE WORLDWIDE
    # ============================================================

    {
        "name": "RemoteOK",
        "type": "json_remoteok",
        "url": "https://remoteok.com/api",
        "region": "remote_worldwide",
    },

    {
        "name": "Remotive",
        "type": "json_remotive",
        # remotive.com/feed (RSS) was retired; this is their current
        # public JSON API, confirmed live 2026-10.
        "url": "https://remotive.com/api/remote-jobs",
        "region": "remote_worldwide",
    },

    {
        "name": "Himalayas",
        "type": "json_himalayas",
        "url": "https://himalayas.app/jobs/api?limit=100",
        "region": "remote_worldwide",
    },

    {
        "name": "Jobicy",
        "type": "json_jobicy",
        "url": "https://jobicy.com/api/v2/remote-jobs?count=100",
        "region": "remote_worldwide",
    },

    {
        "name": "Working Nomads",
        "type": "json_working_nomads",
        "url": "https://www.workingnomads.com/api/exposed_jobs/",
        "region": "remote_worldwide",
    },

    # Remote.co and Wellfound have no confirmed public RSS/JSON feed as of
    # 2026-10 (checked before adding other sources below) — leave the URL
    # blank rather than guess; active_sources() skips them until one is
    # confirmed and filled in.
    {
        "name": "Remote.co",
        "type": "rss",
        "url": "",
        "region": "remote_worldwide",
    },

    {
        "name": "Wellfound",
        "type": "rss",
        "url": "",
        "region": "remote_worldwide",
    },

    # ============================================================
    # LEGIT ATS BOARDS — same spirit as the Greenhouse/80,000 Hours
    # job search: individual, verified employers rather than a scraped
    # aggregator. my.greenhouse.io and jobs.80000hours.org have no public
    # feed to poll (checked 2026-10), so instead we poll each ATS
    # provider's own public per-company Job Board API directly. Every
    # URL below was confirmed live with a direct request before being
    # added. Add more companies by finding their board token/account
    # slug (usually visible in their careers URL) and confirming the
    # same API pattern returns HTTP 200.
    # ============================================================

    {
        "name": "Remote.com (Greenhouse)",
        "type": "json_greenhouse",
        "url": "https://boards-api.greenhouse.io/v1/boards/remotecom/jobs",
        "region": "mixed",
    },

    {
        "name": "GitLab (Greenhouse)",
        "type": "json_greenhouse",
        "url": "https://boards-api.greenhouse.io/v1/boards/gitlab/jobs",
        "region": "mixed",
    },

    {
        "name": "Wise (Greenhouse)",
        "type": "json_greenhouse",
        "url": "https://boards-api.greenhouse.io/v1/boards/wise/jobs",
        "region": "mixed",
    },

    {
        "name": "Stripe (Greenhouse)",
        "type": "json_greenhouse",
        "url": "https://boards-api.greenhouse.io/v1/boards/stripe/jobs",
        "region": "mixed",
    },

    {
        "name": "Moniepoint (Greenhouse)",
        "type": "json_greenhouse",
        "url": "https://boards-api.greenhouse.io/v1/boards/moniepoint/jobs",
        "region": "mixed",
    },

    {
        "name": "Sticker Mule (Ashby)",
        "type": "json_ashby",
        "url": "https://api.ashbyhq.com/posting-api/job-board/stickermule",
        "region": "mixed",
    },

    {
        "name": "Zapier (Ashby)",
        "type": "json_ashby",
        "url": "https://api.ashbyhq.com/posting-api/job-board/zapier",
        "region": "mixed",
    },

    {
        "name": "M-KOPA (Ashby)",
        "type": "json_ashby",
        "url": "https://api.ashbyhq.com/posting-api/job-board/M-KOPA",
        "region": "mixed",
    },

    {
        "name": "Hospitable (Workable)",
        "type": "json_workable",
        "url": "https://apply.workable.com/api/v1/widget/accounts/hospitable",
        "region": "mixed",
    },

    {
        "name": "NALA (Workable)",
        "type": "json_workable",
        "url": "https://apply.workable.com/api/v1/widget/accounts/nalamoney",
        "region": "mixed",
    },

    {
        "name": "Carry1st (Workable)",
        "type": "json_workable",
        "url": "https://apply.workable.com/api/v1/widget/accounts/carry1st",
        "region": "mixed",
    },
]


# ---------------------------------------------------------------------------
# Software development roles
# ---------------------------------------------------------------------------

KEYWORDS = [
    # Software engineering
    "software engineer",
    "software developer",
    "software development engineer",
    "software programmer",
    "application developer",
    "application engineer",

    # Backend
    "backend engineer",
    "backend developer",
    "back-end engineer",
    "back-end developer",
    "back end engineer",
    "back end developer",

    # Full stack
    "full stack engineer",
    "full-stack engineer",
    "fullstack engineer",
    "full stack developer",
    "full-stack developer",
    "fullstack developer",

    # Frontend
    "frontend engineer",
    "frontend developer",
    "front-end engineer",
    "front-end developer",
    "front end engineer",
    "front end developer",

    # Web
    "web developer",
    "web engineer",

    # PHP
    "php developer",
    "php engineer",
    "php backend developer",
    "laravel developer",
    "laravel engineer",
    "laravel backend developer",

    # JavaScript / TypeScript
    "javascript developer",
    "javascript engineer",
    "typescript developer",
    "typescript engineer",

    # React
    "react developer",
    "react engineer",
    "react.js developer",
    "react.js engineer",

    # Node
    "node developer",
    "node engineer",
    "node.js developer",
    "node.js engineer",
    "nodejs developer",
    "nodejs engineer",

    # Python
    "python developer",
    "python engineer",
    "python backend developer",

    # Go
    "golang developer",
    "golang engineer",
    "go developer",
    "go engineer",

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