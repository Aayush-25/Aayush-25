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
git add README.md SETUP.md .github/workflows/snake.yml .github/workflows/update-activity.yml scripts/update_readme.py
git commit -m "feat: add profile README with stats, snake, and activity auto-update"
git branch -M main
git remote add origin https://github.com/Aayush-25/Aayush-25.git
git push -u origin main
```

---

## Step 3 — Enable GitHub Actions write permissions (required for both workflows)

1. Go to your repo: `github.com/Aayush-25/Aayush-25`
2. Click **Settings** → **Actions** → **General**
3. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
4. Click **Save**

Both workflows (`snake.yml` and `update-activity.yml`) require this. One setting covers both.

---

## Step 4 — Run the snake workflow manually (first time)

The snake runs on a schedule (every 12 hours) but trigger it now so the SVG exists immediately:

1. Go to **Actions** tab in your repo
2. Click **Generate Snake Animation** in the left sidebar
3. Click **Run workflow** → **Run workflow** (green button)
4. Wait ~30 seconds — a new `output` branch will appear with the generated SVGs

The snake embed in the README will start rendering once this branch exists.

---

## Step 5 — Run the activity update workflow manually (first time)

This workflow replaces the `<!--LAST_PUSH-->` placeholder in the README with your real last push event. Run it once immediately so the terminal block shows live data instead of the placeholder:

1. Go to **Actions** tab
2. Click **Update Activity** in the left sidebar
3. Click **Run workflow** → **Run workflow**
4. Wait ~20 seconds — it will commit an updated README if you have any public push events

After this, it runs automatically every 6 hours.

---

## Step 6 — Pin the right 6 repositories

1. Go to your GitHub profile: `github.com/Aayush-25`
2. Click **Customize your pins** (below the bio section)
3. Pin these 6 repos in this order:

| # | Repo | Signal |
|---|------|--------|
| 1 | `Aayush-25/EvalOps` | Flagship LLM eval platform |
| 2 | `Aayush-25/NEXUS` | Research — ICCCNet 2026 |
| 3 | `Aayush-25/JobFlowQ` | Distributed systems / Java |
| 4 | `Aayush-25/FrameWatch` | ML/CV — YOLOv8, 84% accuracy |
| 5 | `Aayush-25/ResumeAI` | Live product on Vercel |
| 6 | `Aayush-25/OrderFlow` | Data engineering / ETL |

---

## Step 7 — Verify everything is live

| Widget | Where to check |
|--------|---------------|
| Typing animation | Profile homepage — should cycle through 4 roles |
| skillicons rows | Profile homepage — three rows of tech icons |
| Pin cards (EvalOps, NEXUS, JobFlowQ, FrameWatch) | Profile homepage — dark cards with purple border |
| Stats + Top Langs | Profile homepage — side by side, tokyonight theme |
| Trophies | Profile homepage — tokyonight theme, 7 columns |
| Snake animation | Profile homepage — after Step 4 workflow completes |
| Activity line | Terminal block — after Step 5 workflow completes |
| Visitor badge | Top of profile — increments on each visit |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Snake SVG is broken | Run the snake workflow manually (Step 4) and wait for the `output` branch |
| `last_push` still shows `<!--LAST_PUSH-->` | Run the Update Activity workflow manually (Step 5) |
| Stats card shows an error | `github-readme-stats.vercel.app` is rate-limited — wait 2–3 min and hard-refresh |
| Trophies don't appear | Account needs some commit/star activity to populate; check back after pushing to a few repos |
| Actions tab doesn't show the workflows | Confirm write permissions are set (Step 3) and the push in Step 2 succeeded |
| Profile README not showing | The repo name **must exactly match** your username: `Aayush-25` |
