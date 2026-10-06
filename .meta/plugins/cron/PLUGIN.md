# cron: time-automation territory

## Design Overview

- **Why it exists**: the 'cadence' of scheduled tasks was once scattered across three places (lark-calendar's session-edition daily refresh, email's optional daily refresh, bili digest reserved), while the executors (harness scheduler / system task scheduler) are per-workspace, machine-bound, and lost on machine change or reinstall — the intent of 'what should be automated when' had no home: the execution side had tasks but no archive, the wiki side had disclosures but no registry. This plugin gives the intent an md home
- **Key rulings**:
  - **Declaration-as-source, executor-as-projection**: an extension of three-projections-one-source into the execution dimension, dissolving the constitutional-principle-4 tension (harness replaceable) — the crontab 5-field semantics are the cross-harness lingua franca, the translation rule belonging to the replay recipe; changing harness / machine = read the declaration pages and replay
  - **One page per task, pure-directory scheme** (user ruling 2026-10-06, the single-declaration-page proposal rejected): the directory is the full declaration set, no root declaration page — contrast with why the project domain needs `wiki/projects.md` (its container lies outside wiki), while cron task pages are already inside wiki; quick views go through the derived index page
  - **Reconciliation + replay** (user ruling): the declaration is the source of truth — drift enters the check attached audit (declaration page set ↔ harness task list ↔ system task list, three-way diff), the replay recipe standardized; writing system state and deleting/stopping execution-side tasks both go through user confirmation (following the device attached-audit delegation precedent)
  - **Execution-shape dichotomy lifted** (generalized from the bili ruling into a global criterion): any agent-judgment step → session (unattended session); purely mechanical → script (system task running a connector subcommand, zero quota) — each domain merely tags form, no longer inventing its own cadence disclosures
  - **Unified failure discipline** (lifted from lark-calendar): failed sources report via log, never blocking other tasks; repair delegations one-way derive into todo
  - **Unattended-session SASU-L**: an agent woken by the scheduler has zero priors — at replay the prompt must be self-contained (read the task page and execute per the page + report failures via log); the recipe belongs to this plugin's usage; this is the application of 'no knowledge layer leaking into the architecture' at the session boundary
  - **machine anchor left blank**: locates the executing machine in multi-device deployments; v0.1 keeps only the optional key, no device linkage built; refine through use
- **Position in the family**: a global plugin (cross-cutting time automation), not a domain plugin, does not depend on domain; domain plugins attach and register via the on-demand bridge — this plugin holds 'who is present, when it runs, how to replay and reconcile'; task action shapes belong to each domain (the principle-11 bridge philosophy)

## Structure

- `wiki/cron/<task name>.md` — task page: `cron` block mapping mechanical zone (schedule / action / form / domain / status / last_run / machine optional) + two body sections — `## Task` (action details: which command to call or what the session opening reads, back-linking the owning domain's skill), `## Run Notes` (append-only and convergent: anomalies, repairs, change decisions; normal runs unrecorded — log already has lines, to prevent bloat)
- No root declaration page: the directory is the full set; the derived index includes quick views

## Invariants

- Declaration-as-source: the execution side (harness scheduler / system task scheduler) is a replaceable projection; replay and reconciliation both defer to the declaration pages
- System-state writes require user confirmation: the script edition landing system tasks, status changes syncing deletes/stops on the execution side — following the device attached-audit delegation precedent
- Normal runs write no task-page history; run notes take only anomalies and changes; last_run is machine-maintained
- status: paused / deprecated pages are never deleted (kept for the record); deprecated tasks remain in the directory for lineage reference
- Three-way boundary: todo one-shot delegations · calendar event facts (what happens when) · cron recurring automation intent (what to automate when); task outputs land per each domain's discipline (e.g. lark-calendar's daily-refresh output goes into the month page's schedule section, bili digest refreshes the digest page)

## Changelog

- 0.3 (2026-10-06) inject line: sections lost to the kernel comment-strip clip restored (quoted values are now protected), tightened for budget headroom — issue #12 post-migration nit- 0.2 (2026-10-06) inject line compressed to pointer density (issue #12 layer discipline) — procedural detail lives in usage / PLUGIN.md / skills- 0.1 2026-10-06: established — three questions converged (a unified registry covering both session/script shapes, reconciliation + replay, one page per task); lark-calendar 0.2 / bili 0.2 / email 0.4 moved along with the bridge attachment (scattered cadence disclosures rewritten into place)
