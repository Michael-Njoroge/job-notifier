"""
Daily developer job notifier.

Fetches jobs from RSS/JSON sources, filters them for relevant
software-development roles, skips previously notified jobs,
and sends a formatted HTML digest via Telegram and/or Resend.
"""

import html
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import feedparser
import requests
from dotenv import load_dotenv

from config import (
    EXCLUDED_KEYWORDS,
    KENYA_KEYWORDS,
    KEYWORDS,
    REMOTE_KEYWORDS,
    active_sources,
)
from sources.linkedin import get_linkedin_searches


load_dotenv()


SEEN_FILE = Path(__file__).parent / "seen.json"

MAX_SEEN = 1000
REQUEST_TIMEOUT = 15

USER_AGENT = "job-notifier/1.0 (personal use; daily run)"


# ============================================================================
# Seen jobs
# ============================================================================

def load_seen() -> set:
    if not SEEN_FILE.exists():
        return set()

    try:
        return set(json.loads(SEEN_FILE.read_text()))
    except (json.JSONDecodeError, OSError):
        return set()


def save_seen(seen: set) -> None:
    trimmed = list(seen)[-MAX_SEEN:]

    SEEN_FILE.write_text(
        json.dumps(
            trimmed,
            indent=2,
        )
    )


# ============================================================================
# Filtering
# ============================================================================

def contains_excluded_keyword(text: str) -> bool:
    text = text.lower()

    return any(
        keyword.lower() in text
        for keyword in EXCLUDED_KEYWORDS
    )


def matches_keywords(title: str) -> bool:
    """
    Return True only when the job title looks like a software
    development role and isn't an explicitly excluded role.
    """

    title = title.strip()

    if not title:
        return False

    if contains_excluded_keyword(title):
        return False

    title_lower = title.lower()

    return any(
        keyword.lower() in title_lower
        for keyword in KEYWORDS
    )


def get_match_score(title: str) -> int:
    """
    Title-based relevance score.

    This is not an AI score. It simply helps rank the strongest
    software-development matches near the top of the email.
    """

    title_lower = title.lower()

    if contains_excluded_keyword(title):
        return 0

    if not matches_keywords(title):
        return 0

    score = 60

    strong_matches = [
        "software engineer",
        "software developer",
        "full stack engineer",
        "full-stack engineer",
        "full stack developer",
        "full-stack developer",
        "backend engineer",
        "backend developer",
        "frontend engineer",
        "frontend developer",
        "laravel",
        "php",
        "react",
        "typescript",
        "node.js",
        "nodejs",
    ]

    for keyword in strong_matches:
        if keyword in title_lower:
            score += 5

    if "senior" in title_lower:
        score += 8

    if "staff" in title_lower:
        score += 7

    if "principal" in title_lower:
        score += 7

    if "lead" in title_lower:
        score += 5

    return min(score, 100)


# ============================================================================
# Location filtering
# ============================================================================

def contains_any(text: str, keywords: list[str]) -> bool:
    text_lower = text.lower()

    return any(
        keyword.lower() in text_lower
        for keyword in keywords
    )


def is_kenya_job(job: dict) -> bool:
    """
    Determine whether a job appears to be Kenya-related.
    """

    location_text = " ".join(
        [
            str(job.get("location", "")),
            str(job.get("description", "")),
            str(job.get("title", "")),
        ]
    )

    return contains_any(
        location_text,
        KENYA_KEYWORDS,
    )


def is_remote_job(job: dict) -> bool:
    """
    Determine whether a job appears to be remote.
    """

    location_text = " ".join(
        [
            str(job.get("location", "")),
            str(job.get("description", "")),
            str(job.get("title", "")),
        ]
    )

    return contains_any(
        location_text,
        REMOTE_KEYWORDS,
    )


def is_relevant_job(job: dict, source: dict) -> bool:
    """
    Final job filter.

    Kenya sources:
        Accept the job because the source itself is Kenya-focused.

    Remote sources:
        Accept jobs that are marked/identified as remote.

    In both cases:
        The title must be a software-development role.
    """

    title = job.get("title", "")

    if not matches_keywords(title):
        return False

    region = source.get("region")

    if region == "kenya":
        return True

    if region == "remote_worldwide":
        return is_remote_job(job)

    return True


# ============================================================================
# Fetching
# ============================================================================

def fetch_rss(url: str) -> list[dict]:
    feed = feedparser.parse(
        url,
        request_headers={
            "User-Agent": USER_AGENT,
        },
    )

    jobs = []

    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()

        if not title or not link:
            continue

        description = (
            entry.get("summary")
            or entry.get("description")
            or ""
        )

        jobs.append(
            {
                "title": title,
                "link": link,
                "description": description,
                "location": "",
            }
        )

    return jobs


def fetch_remoteok(url: str) -> list[dict]:
    response = requests.get(
        url,
        headers={
            "User-Agent": USER_AGENT,
        },
        timeout=REQUEST_TIMEOUT,
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    # RemoteOK's first element is metadata.
    for item in data[1:]:
        title = (
            item.get("position")
            or item.get("title")
            or ""
        ).strip()

        link = (
            item.get("url")
            or ""
        ).strip()

        if not title or not link:
            continue

        description = (
            item.get("description")
            or ""
        )

        location = (
            item.get("location")
            or ""
        )

        jobs.append(
            {
                "title": title,
                "link": link,
                "description": description,
                "location": location,
            }
        )

    return jobs


def fetch_source(source: dict) -> list[dict]:
    try:
        if source["type"] == "rss":
            return fetch_rss(
                source["url"]
            )

        if source["type"] == "json_remoteok":
            return fetch_remoteok(
                source["url"]
            )

    except Exception as error:
        print(
            f"[warn] {source['name']} failed: {error}",
            file=sys.stderr,
        )

    return []


# ============================================================================
# Telegram
# ============================================================================

def send_telegram(message: str) -> bool:
    token = os.environ.get(
        "TELEGRAM_BOT_TOKEN"
    )

    chat_id = os.environ.get(
        "TELEGRAM_CHAT_ID"
    )

    if not token or not chat_id:
        return False

    chunk_size = 3500

    success = True

    for start in range(
        0,
        len(message),
        chunk_size,
    ):
        chunk = message[
            start:start + chunk_size
        ]

        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={
                "chat_id": chat_id,
                "text": chunk,
                "disable_web_page_preview": True,
            },
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code != 200:
            print(
                "[warn] Telegram send failed: "
                f"{response.status_code} "
                f"{response.text}",
                file=sys.stderr,
            )

            success = False

        time.sleep(1)

    return success


# ============================================================================
# Email helpers
# ============================================================================

def job_card(job: dict) -> str:
    title = html.escape(
        job["title"]
    )

    link = html.escape(
        job["link"],
        quote=True,
    )

    source = html.escape(
        job.get(
            "source",
            "Job Board",
        )
    )

    score = job.get(
        "score",
        50,
    )

    if score >= 90:
        badge = "🔥 Excellent Match"
        badge_color = "#047857"

    elif score >= 75:
        badge = "⭐ Strong Match"
        badge_color = "#2563eb"

    else:
        badge = "✓ Relevant"
        badge_color = "#64748b"

    return f"""
<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="
         margin:0 0 14px 0;
         border:1px solid #e2e8f0;
         border-radius:12px;
         background:#ffffff;
       ">
<tr>
<td style="padding:20px 22px;">

<div style="
  display:inline-block;
  margin-bottom:10px;
  padding:5px 9px;
  border-radius:999px;
  background:#f1f5f9;
  color:{badge_color};
  font-size:12px;
  font-weight:700;
">
  {badge} · {score}%
</div>

<div style="
  font-size:18px;
  line-height:1.4;
  font-weight:700;
  color:#0f172a;
  margin-bottom:6px;
">
  {title}
</div>

<div style="
  font-size:13px;
  color:#64748b;
  margin-bottom:15px;
">
  {source}
</div>

<a href="{link}"
   style="
     display:inline-block;
     padding:10px 15px;
     background:#111827;
     color:#ffffff;
     text-decoration:none;
     border-radius:7px;
     font-size:13px;
     font-weight:700;
   ">
  View Job →
</a>

</td>
</tr>
</table>
"""


def build_linkedin_section() -> str:
    searches = get_linkedin_searches()

    kenya = [
        search
        for search in searches
        if search["location"] == "Kenya"
    ]

    remote = [
        search
        for search in searches
        if search["location"] == "Worldwide"
    ]

    def build_links(items):
        rows = []

        for item in items:
            name = html.escape(
                item["name"]
            )

            url = html.escape(
                item["url"],
                quote=True,
            )

            rows.append(
                f"""
<tr>
<td style="padding:6px 0;">
<a href="{url}"
   style="
     color:#2563eb;
     text-decoration:none;
     font-size:14px;
     font-weight:600;
   ">
  {name} →
</a>
</td>
</tr>
"""
            )

        return "".join(rows)

    return f"""
<h2 style="
  margin:30px 0 12px 0;
  font-size:17px;
  color:#0f172a;
">
  🔎 LinkedIn Searches
</h2>

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="
         border:1px solid #e2e8f0;
         border-radius:12px;
         background:#ffffff;
       ">

<tr>
<td style="padding:20px 22px;">

<div style="
  font-size:14px;
  font-weight:800;
  color:#334155;
  margin-bottom:8px;
">
  🇰🇪 Kenya
</div>

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0">
  {build_links(kenya)}
</table>

<div style="
  margin-top:20px;
  font-size:14px;
  font-weight:800;
  color:#334155;
  margin-bottom:8px;
">
  🌍 Remote
</div>

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0">
  {build_links(remote)}
</table>

</td>
</tr>

</table>
"""


def build_html(
    new_jobs_by_source: dict,
) -> str:

    all_jobs = []

    for source_name, jobs in (
        new_jobs_by_source.items()
    ):
        for job in jobs:
            job["source"] = source_name

            job["score"] = get_match_score(
                job["title"]
            )

            all_jobs.append(job)

    all_jobs.sort(
        key=lambda job: job["score"],
        reverse=True,
    )

    total = len(all_jobs)

    top_jobs = all_jobs[:5]

    remaining_jobs = all_jobs[5:]

    top_cards = "".join(
        job_card(job)
        for job in top_jobs
    )

    grouped = {}

    for job in remaining_jobs:
        grouped.setdefault(
            job["source"],
            [],
        ).append(job)

    source_sections = []

    for source_name, jobs in (
        grouped.items()
    ):
        cards = "".join(
            job_card(job)
            for job in jobs
        )

        source_sections.append(
            f"""
<h2 style="
  margin:28px 0 12px 0;
  font-size:16px;
  color:#334155;
">
  {html.escape(source_name)}

  <span style="
    font-size:12px;
    color:#94a3b8;
    font-weight:400;
  ">
    · {len(jobs)} jobs
  </span>
</h2>

{cards}
"""
        )

    other_sections = "".join(
        source_sections
    )

    linkedin_section = (
        build_linkedin_section()
    )

    today = datetime.now().strftime(
        "%A, %d %B %Y"
    )

    job_word = (
        "job"
        if total == 1
        else "jobs"
    )

    return f"""
<!DOCTYPE html>

<html>

<head>
<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0">

<title>
Daily Developer Job Digest
</title>
</head>

<body style="
  margin:0;
  padding:0;
  background:#f1f5f9;
  font-family:
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    Arial,
    sans-serif;
  color:#0f172a;
">

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="background:#f1f5f9;">

<tr>

<td align="center"
    style="padding:28px 12px;">

<table role="presentation"
       width="100%"
       cellpadding="0"
       cellspacing="0"
       style="
         max-width:680px;
         background:#ffffff;
         border-radius:16px;
         overflow:hidden;
       ">


<!-- ========================================================= -->
<!-- HEADER -->
<!-- ========================================================= -->

<tr>

<td style="
  padding:30px;
  background:#111827;
  color:#ffffff;
">

<div style="
  font-size:12px;
  letter-spacing:1.5px;
  font-weight:800;
  color:#94a3b8;
  margin-bottom:8px;
">
  💼 DAILY JOB DIGEST
</div>

<div style="
  font-size:28px;
  line-height:1.2;
  font-weight:800;
  margin-bottom:8px;
">
  Your developer opportunities
</div>

<div style="
  font-size:14px;
  color:#cbd5e1;
">
  Kenya + Remote opportunities
</div>

<div style="
  font-size:13px;
  color:#94a3b8;
  margin-top:7px;
">
  {today}
</div>

</td>

</tr>


<!-- ========================================================= -->
<!-- SUMMARY -->
<!-- ========================================================= -->

<tr>

<td style="
  padding:25px 30px 12px 30px;
">

<div style="
  font-size:24px;
  font-weight:800;
  color:#0f172a;
">
  {total} new {job_word}
</div>

<div style="
  margin-top:5px;
  font-size:14px;
  line-height:1.6;
  color:#64748b;
">
  Software engineering and development opportunities
  matching your search criteria.
</div>

</td>

</tr>


<!-- ========================================================= -->
<!-- TOP MATCHES -->
<!-- ========================================================= -->

<tr>

<td style="
  padding:0 30px;
">

<h2 style="
  margin:20px 0 14px 0;
  font-size:17px;
  color:#0f172a;
">
  🔥 Top Matches
</h2>

{top_cards}

</td>

</tr>


<!-- ========================================================= -->
<!-- OTHER JOBS -->
<!-- ========================================================= -->

<tr>

<td style="
  padding:0 30px 10px 30px;
">

{other_sections}

</td>

</tr>


<!-- ========================================================= -->
<!-- LINKEDIN -->
<!-- ========================================================= -->

<tr>

<td style="
  padding:0 30px 20px 30px;
">

{linkedin_section}

</td>

</tr>


<!-- ========================================================= -->
<!-- FOOTER -->
<!-- ========================================================= -->

<tr>

<td style="
  padding:24px 30px;
  background:#f8fafc;
  border-top:1px solid #e2e8f0;
  text-align:center;
">

<div style="
  font-size:13px;
  font-weight:700;
  color:#334155;
  margin-bottom:6px;
">
  Job Notifier
</div>

<div style="
  font-size:12px;
  color:#94a3b8;
  line-height:1.6;
">
  Automated daily developer job search.<br>
  Kenya + remote opportunities.
</div>

</td>

</tr>

</table>

</td>

</tr>

</table>

</body>

</html>
"""


# ============================================================================
# Resend
# ============================================================================

def send_email_resend(
    subject: str,
    html_body: str,
) -> bool:

    api_key = os.environ.get(
        "RESEND_API_KEY"
    )

    email_from = os.environ.get(
        "EMAIL_FROM"
    )

    email_to = os.environ.get(
        "EMAIL_TO"
    )

    if not (
        api_key
        and email_from
        and email_to
    ):
        print(
            "[warn] Resend environment variables "
            "are not configured.",
            file=sys.stderr,
        )

        return False

    response = requests.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "from": email_from,
            "to": [email_to],
            "subject": subject,
            "html": html_body,
        },
        timeout=REQUEST_TIMEOUT,
    )

    if response.status_code not in (
        200,
        201,
    ):
        print(
            "[warn] Resend email failed: "
            f"{response.status_code} "
            f"{response.text}",
            file=sys.stderr,
        )

        return False

    return True


# ============================================================================
# Main
# ============================================================================

def main() -> None:

    seen = load_seen()

    new_jobs_by_source = {}

    for source in active_sources():

        print(
            f"[info] Checking {source['name']}..."
        )

        jobs = fetch_source(source)

        print(
            f"[info] {source['name']}: "
            f"{len(jobs)} jobs fetched."
        )

        new_matches = []

        for job in jobs:

            job_id = job["link"]

            if job_id in seen:
                continue

            if not is_relevant_job(
                job,
                source,
            ):
                continue

            new_matches.append(job)

        if new_matches:

            new_jobs_by_source[
                source["name"]
            ] = new_matches

            print(
                f"[info] {source['name']}: "
                f"{len(new_matches)} new matches."
            )

        time.sleep(2)

    if not new_jobs_by_source:

        print(
            "No new matching jobs today."
        )

        return

    total = sum(
        len(jobs)
        for jobs in (
            new_jobs_by_source.values()
        )
    )

    # ------------------------------------------------------------
    # Telegram message
    # ------------------------------------------------------------

    lines = [
        "🧑‍💻 NEW DEVELOPER JOBS",
        "",
        f"{total} new relevant job(s)",
        "",
    ]

    for source_name, jobs in (
        new_jobs_by_source.items()
    ):

        lines.append(
            f"— {source_name} —"
        )

        for job in jobs:

            lines.append(
                f"• {job['title']}\n"
                f"  {job['link']}"
            )

        lines.append("")

    message = "\n".join(lines)

    # ------------------------------------------------------------
    # Email
    # ------------------------------------------------------------

    html_body = build_html(
        new_jobs_by_source
    )

    sent_telegram = send_telegram(
        message
    )

    sent_email = send_email_resend(
        subject=(
            f"💼 {total} New Developer Job"
            + (
                "s"
                if total != 1
                else ""
            )
        ),
        html_body=html_body,
    )

    # ------------------------------------------------------------
    # Mark seen ONLY after notification succeeds
    # ------------------------------------------------------------

    if sent_telegram or sent_email:

        for jobs in (
            new_jobs_by_source.values()
        ):
            for job in jobs:
                seen.add(
                    job["link"]
                )

        save_seen(seen)

        channels = ", ".join(
            channel
            for channel, sent in [
                (
                    "Telegram",
                    sent_telegram,
                ),
                (
                    "email",
                    sent_email,
                ),
            ]
            if sent
        )

        print(
            f"Sent notification for "
            f"{total} new job(s) via "
            f"{channels}."
        )

    else:

        print(
            "[warn] No notification channel "
            "succeeded."
        )

        print(
            "Jobs were NOT marked as seen."
        )

        print(message)


if __name__ == "__main__":
    main()