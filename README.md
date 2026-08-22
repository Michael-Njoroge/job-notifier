# 💼 Daily Developer Job Notifier

A lightweight Python job-search notifier that automatically finds **software development opportunities in Kenya and remote roles worldwide**, filters out irrelevant positions, and sends a clean daily digest through **email and/or Telegram**.

The project is designed to run automatically using **GitHub Actions**, so no server or VPS is required.

---

## ✨ What It Does

Every day, the notifier:

1. Fetches jobs from supported public RSS/JSON feeds.
2. Filters listings for software-development roles.
3. Removes irrelevant roles such as:
   - DevOps
   - SRE
   - QA
   - Product Management
   - Business Development
   - Customer Support
   - Data Science
   - Mobile Development
   - Internships
4. Detects jobs that have not previously been sent.
5. Scores jobs based on title relevance.
6. Builds a formatted HTML email.
7. Sends the digest through:
   - Email via Resend
   - Telegram
8. Includes targeted LinkedIn search links for:
   - 🇰🇪 Kenya
   - 🌍 Remote worldwide
9. Stores previously notified jobs in `seen.json`.
10. Runs automatically every morning through GitHub Actions.

---

# 🎯 Target

The notifier is intentionally focused on:

### 🇰🇪 Kenya

Jobs based in:

- Nairobi
- Mombasa
- Kisumu
- Nakuru
- Eldoret
- Kiambu
- Machakos
- Thika
- Anywhere else in Kenya

Including:

- On-site
- Hybrid
- Remote

### 🌍 Remote Worldwide

International remote opportunities where the job can genuinely be performed remotely.

The goal is **not** to fill the inbox with random remote jobs that are restricted to a particular country.

---

# 🧑‍💻 Target Roles

The primary target is software development.

Examples:

- Software Engineer
- Software Developer
- Full Stack Developer
- Full Stack Engineer
- Backend Developer
- Backend Engineer
- Frontend Developer
- Frontend Engineer
- Web Developer
- Web Engineer
- PHP Developer
- Laravel Developer
- React Developer
- TypeScript Developer
- Node.js Developer
- Application Developer
- Technical Lead
- Tech Lead

The keyword list can be changed in:

```text
config.py