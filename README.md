# claude-plugins

A personal claude.ai plugin marketplace.

## nature-skills

`plugins/nature-skills/` holds 13 skills copied from
[Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills)
(Apache-2.0, © Yizhe Yuan and Nature Skills contributors; license in
`plugins/nature-skills/LICENSE`).

Changes from upstream: only the skills listed in
`scripts/sync_nature_skills.py` are copied, and a short Chinese label
followed by `｜` is added to the start of each skill's `description`.
`plugins/nature-skills/UPSTREAM_COMMIT` records the upstream commit copied.

The workflow `.github/workflows/sync-nature-skills.yml` refreshes the copy
every day at 04:17 Japan time; run it by hand from the Actions tab with
**Run workflow**. To add or remove a skill, edit `LABELS` in
`scripts/sync_nature_skills.py`. A skill removed from `LABELS` stops being
updated but its folder stays until it is deleted by hand.
