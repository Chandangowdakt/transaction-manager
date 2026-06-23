# Quick Deploy Guide (~10 minutes)

Follow these steps to get live URLs for your submission.

## Step 1 — Push to GitHub ✅ Done

Repo: https://github.com/Chandangowdakt/transaction-manager

## Step 2 — Deploy Backend on Render (free)

1. Sign up / log in at https://render.com
2. Click **New** → **Blueprint**
3. Connect your GitHub repo
4. Render detects `render.yaml` — click **Apply**
5. Wait ~2 min for deploy. Copy your service URL (e.g. `https://transaction-api.onrender.com`)

## Step 3 — Update Frontend Backend URL

If your Render URL is **not** `https://transaction-api.onrender.com`, edit `frontend/index.html` line ~193:

```javascript
return "https://YOUR-ACTUAL-RENDER-URL.onrender.com";
```

Commit and push:

```bash
git add frontend/index.html
git commit -m "Point frontend at deployed backend"
git push
```

## Step 4 — Enable GitHub Pages (frontend)

1. Repo **Settings** → **Pages**
2. **Source**: GitHub Actions
3. Push to `main` triggers `.github/workflows/pages.yml`
4. After ~1 min, your live frontend is at:
   `https://chandangowdakt.github.io/transaction-manager/`

## Step 5 — Test Live

1. Open your GitHub Pages URL
2. Credit $100 to user `alice`
3. Refresh leaderboard
4. Wake Render first if cold — first request may take ~60 sec

## Step 6 — Record Video

Use [VIDEO_SCRIPT.md](VIDEO_SCRIPT.md) — 3–5 min walkthrough of the **live** app.

## Step 7 — Submit

- GitHub repo link: `https://github.com/Chandangowdakt/transaction-manager`
- Or zip: `ass1-submission.zip` (in your Downloads folder)
- Video link (YouTube unlisted / Drive / Loom)

## Update README Live Links

After deploy, add your URLs to the README **Live Demo** table and commit.
