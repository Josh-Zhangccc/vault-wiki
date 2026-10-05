# Disclosure paradigm: SASU-L and the zero-contamination discipline

> Ruling of 2026-09-12: with the project positioned for personal use, the test-set matrix and cross-validation protocol were abolished (never executed; the design is preserved in git history). This document retains the SASU-L disclosure paradigm and the zero-contamination discipline, as a mirror for writing skills / docs and for self-review.
> Basis (two rounds of empirical work on 2026-09-12: cold start on a fictional vault, migration of 25 items in a real vault): in real deployments the agent knows things only in SASU-L order, with zero priors; every "assumed known" in the framework is non-portable knowledge-layer leakage (an extension of the principle-2 touchstone). Empirical regularities—wrong-guess points = where the spec lacks examples; behavioral divergence points = where rules are absent from the execution site; silent rot = where formal-layer feedback is missing.

## SASU-L: the environment's only disclosure channel

1. **S** (system prompt) — the harness base: identity, toolset, general behavioral rules. Outside the framework's control; treat it as the given environment; differences in S across harnesses are not charged to the framework's account (including whether AGENTS.md is auto-injected at all—that too is an S-layer property)
2. **A** (AGENTS.md) — the workspace constitution: system-injected, including the plugin injection region—identity, principles, structural map
3. **S** (Skills) — the capability surface: skill **descriptions** are available at session start; bodies load on trigger—the actual reading happens inside L
4. **U** (user prompt) — the user's own words: the sole legitimate source of task semantics
5. **L** (loop) — the execute-observe cycle: reading anchors, reading pages, calling tools, post-write feedback. Anchors and pages (registry, vocabulary, PLUGIN.md, hot, index, pre-existing pages) are **resources accessed within L, not standalone stages**; **pre-existing pages are part of the spec**—the agent uses existing pages as format references (empirically: multiple sessions in the migration experiment consulted precedent pages to align format), hence gold-sample quality is disclosure quality

The first four links are a static availability ordering; all actual reading happens in L. Any information beyond this—training priors, spec restatements stuffed into prompts, verbal conventions—counts as nonexistent on the agent side.

## Zero-contamination discipline (also used for comparisons and spot checks)

- Cold-start subagent: no conversation history; the prompt contains only two things—what the environment supplies (role positioning + working directory) and the **U-layer original user task text**
- **U-layer purity**: no restating any S / A layer content (e.g. do not write "remember to reuse the vocabulary" or "remember to run the pipeline"—that is the Skills layer's job; restating it inflates the measurement)
- Interaction steps (confirmations / questions) declare their proxy approach under an "experiment protocol" statement, but must not slip in format answers along the way
- When a comparison is needed: run the same type of task before and after the change and compare friction points; running them simultaneously contaminates both

## Validate by use (since 2026-09-12)

Whether a change works is judged by real-use feedback: friction points (guessing formats, missed steps, repeatedly explaining the same thing) are spec voids; fix one spot, use one spot—no matrix thresholds.
