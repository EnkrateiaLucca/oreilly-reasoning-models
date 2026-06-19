# OpenAI Model Currency — `gpt-5.2` → `gpt-5.5`

**Status:** Verified 2026-06-19. Source-of-record for swapping the retired `gpt-5.2` model string to the current `gpt-5.5` across this course.

## Finding

- OpenAI **retired `gpt-5.2` on 2026-06-12**; it is no longer served by the API. [source: https://help.openai.com/en/articles/9624314-model-release-notes]
- The **current API flagship / reasoning model is `gpt-5.5`**, available in the API since 2026-04-24. [source: https://developers.openai.com/api/docs/guides/latest-model]
- `gpt-5.5` keeps the same `reasoning.effort` interface as `gpt-5.2` and supports levels **`none` / `low` / `medium` / `high` / `xhigh`**, with default **`medium`**. [source: https://developers.openai.com/api/docs/models/gpt-5.5]

## Decision

- Swap every `gpt-5.2` model string → `gpt-5.5` course-wide (demo apps, notebooks, cheatsheet).
- The "reasoning effort knobs" slide must list all five levels including **`xhigh`** (`none` / `low` / `medium` / `high` / `xhigh`), default `medium`.
- No code-path changes needed beyond the model string: the `reasoning.effort` interface is unchanged.

## Confidence

All claims above are confirmed against the cited OpenAI sources. Nothing is `[unverified]`.
