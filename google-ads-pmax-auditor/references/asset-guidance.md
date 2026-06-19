# Asset Guidance (judgment layer)

`scripts/analyze_pmax.py` handles everything countable: asset counts vs. targets,
character limits, exact and near-duplicate text, Google's LOW/GOOD/BEST labels,
ad strength, image dimensions and aspect ratios, search-theme coverage, and
tracking config. **Read its JSON first.** This file is for the calls a script
can't make — read it when you're writing the recommendations.

## Reading the performance labels (the backbone)
The script lists every `LOW` asset. That list is your first action, but the label
tells you *that* an asset underperforms, not *why*. For each LOW asset, decide:
- **Text**: is it a near-copy of a stronger one (cannibalizing), off-message, or
  just weak phrasing? Rewrite toward a different angle rather than a synonym swap.
- **Image**: is it low-res/wrong-ratio (the script flags that), or technically
  fine but visually weak (cluttered, off-brand, no clear subject)?
- Don't mass-delete LOW assets to a bare minimum — that starves PMax of
  combinations. Replace, don't just remove.

## Text: variety of angle, not variety of words
Google assembles ads by mixing your assets, so the win is *distinct angles*, not
15 rewordings of the same line. Across the headlines, you want coverage of:
- the core offer / product, a key benefit, an objection-handler (returns,
  warranty, price), social proof, and a clear call to action.
- The near-duplicate flag catches lexical twins; you still have to spot two lines
  that say the same *thing* in different words. Those waste a slot.
- Long headlines should be complete thoughts that stand alone — they often render
  without a description.

**Capitalization note:** Google does *not* require Title Case in PMax. Sentence
case is fine and frequently reads better. Don't flag casing as an error; judge
clarity instead.

## Images & video (visual quality is yours to judge)
The script confirms each image resolves, meets minimum size, and roughly matches
its slot's aspect ratio. It can't see the picture. You assess:
- Clear subject, on-brand, not cluttered; minimal or no text overlay (PMax
  prefers clean imagery and may penalize heavy text).
- Genuine variety across the set — different scenes/compositions, not one photo
  cropped three ways.
- Is there at least one **video**? Without it, Google auto-generates one from your
  images, which is usually weaker than a real video and costs you YouTube quality.

## Audience signals / search themes
Signals don't restrict targeting — they *accelerate learning* by telling Google
where to start. Judge:
- Are the search themes and audiences actually relevant to the asset group's
  products, or generic? A vague signal helps little.
- Is first-party data (customer lists) used where available? It's the most durable
  signal as third-party cookies fade.

## Structure & settings
- **Negative keywords and brand exclusions now exist in PMax** (account-level
  negatives self-serve; campaign-level negatives and brand lists available). If
  brand or irrelevant terms are leaking spend, the fix is to *add* them — this is
  no longer an unavoidable PMax limitation.
- **URL expansion**: the script flags when it's ON. That's not automatically
  wrong, but confirm it isn't sending traffic to thin or off-topic pages; use URL
  exclusions or a page feed to control it.
- **One asset group per distinct theme/margin.** Don't cram unrelated products
  into one group (it muddies the creative and the data), and don't over-split into
  many thin groups that never gather enough signal.

## Pre-launch vs. live
On a brand-new campaign there are no performance labels yet (all PENDING/LEARNING)
and no search-category data. A pre-launch audit is about *coverage and quality*:
counts, character limits, duplicates, image specs, signal strength, tracking. A
live audit adds the performance labels and search themes — which is where the real
optimization leverage is, so push to audit live campaigns with data when you can.
