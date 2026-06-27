# Setup Guide — Aayush-25/Aayush-25 Profile README

Follow these steps in order. Takes ~10 minutes total.

---

## Step 1 — Create the special profile repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Set **Repository name** to exactly: `Aayush-25`
   - GitHub will show a green banner: *"Aayush-25/Aayush-25 is a ✨ special ✨ repository..."*
3. Set visibility to **Public**
4. **Do NOT** check "Initialize this repository with a README" — you'll push your own
5. Click **Create repository**

---

## Step 2 — Initialize and push from this folder

Run these commands from the `Aayush-25/` folder on your Desktop:

```bash
cd ~/Desktop/Aayush-25

git init
git add README.md SETUP.md .github/workflows/snake.yml
git commit -m "feat: add profile README with stats, projects, snake animation"
git branch -M main
git remote add origin https://github.com/Aayush-25/Aayush-25.git
git push -u origin main
```

---

## Step 3 — Enable GitHub Actions permissions (required for snake)

1. Go to your repo: `github.com/Aayush-25/Aayush-25`
2. Click **Settings** → **Actions** → **General**
3. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
4. Click **Save**

---

## Step 4 — Run the snake workflow manually (first time)

The snake workflow runs on a schedule (every 12 hours), but trigger it now so it generates the SVGs immediately:

1. Go to **Actions** tab in your repo
2. Click **Generate Snake Animation** in the left sidebar
3. Click **Run workflow** → **Run workflow** (green button)
4. Wait ~30 seconds for it to finish
5. You'll see a new branch called `output` appear in your repo — that's where the SVGs live

The snake will now appear in your README automatically. It re-runs every 12 hours.

---

## Step 5 — Pin the right 6 repositories

Pinned repos appear on your profile below the README. Do this last, after all repos are public.

1. Go to your GitHub profile: `github.com/Aayush-25`
2. Click **Customize your pins** (appears below the bio section)
3. Pin these 6 repos in this order:

| # | Repo | Why |
|---|------|-----|
| 1 | `Aayush-25/EvalOps` | Flagship project — LLM eval platform |
| 2 | `Aayush-25/NEXUS` | Research paper — ICCCNet 2026 |
| 3 | `Aayush-25/JobFlowQ` | Backend/distributed systems signal |
| 4 | `Aayush-25/FrameWatch` | ML/CV — 84% accuracy YOLOv8 |
| 5 | `Aayush-25/ResumeAI` | Live product on Vercel — full-stack |
| 6 | `Aayush-25/OrderFlow` | Data engineering / ETL pipeline |

---

## Step 6 — Verify everything is live

Check each widget loads correctly:

- **Typing animation**: visible on your profile homepage
- **GitHub Stats card**: loads with your actual commit counts
- **Top Languages card**: shows your language breakdown
- **Trophies**: loads from `github-profile-trophy.vercel.app`
- **Snake animation**: visible after the Actions workflow completes (Step 4)
- **Visitor counter**: increments on each profile visit

If the stats cards show an error, wait 2–3 minutes and hard-refresh. The services occasionally rate-limit.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Snake SVG is broken / not loading | Make sure the `output` branch exists (run the workflow manually per Step 4) |
| Stats card shows "couldn't generate" | `github-readme-stats.vercel.app` is rate-limited — try again in a few minutes |
| Trophies don't appear | Your account may be too new; trophies need some activity to populate |
| Actions won't run | Double-check Step 3 — write permissions must be enabled |
| Profile README not showing | The repo name **must** exactly match your GitHub username: `Aayush-25` |
