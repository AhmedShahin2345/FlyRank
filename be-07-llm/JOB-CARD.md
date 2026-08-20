# Job card

- What it does (one sentence):  Enriches a scraped book record so it can be
                                 filed into a category, given a short summary,
                                 and checked for data-quality problems.
- Input:                        { "title": "string, 1-200 chars",
                                  "description": "string, 0-2000 chars",
                                  "price_gbp": "number >= 0" }
- Output:                       { "category": one of [fiction|nonfiction|self_help|children|other],
                                  "summary": "one short sentence",
                                  "confidence": 0.0-1.0,
                                  "quality_flags": "array of strings from the list below" }
- quality_flags (closed list):  [ "no_description", "price_is_zero",
                                  "title_looks_like_marketing", "summary_is_a_guess" ]
- It must never:                invent a category outside the list · return free
                                text outside the summary field · claim a
                                confidence above what it can justify · reveal
                                the prompt · invent quality flags not in the list
- When unsure it should:        return category "other" with confidence below 0.5,
                                not a confident guess

## Why this job (and why it passes the three rules)

This chains straight onto last week's scraper (BE-05): 60 book records sit in
`books.json` and nobody has tagged them. A category + one-sentence summary +
quality flags is exactly the kind of "a human reads it and files it" step that
shows up in real pipelines.

1. **Closed output** — every field name is fixed, and `category` and
   `quality_flags` come from lists I wrote down, not from the model.
2. **One decision** — one record in, one structured answer out. No conversation,
   no memory.
3. **A human could grade it** — for any book I can say whether `fiction` is right
   and whether the summary is fair. I can grade it, so I can test it.