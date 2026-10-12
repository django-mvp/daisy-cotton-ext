# ADR 0014 — A marquee moves by CSS and can always be stopped

**Status:** accepted

## Decision

`<c-marquee>` is a row that travels across the page and comes round again. The logo blocks are
built on it. The package ships no JavaScript for it. These rules follow, and each is the reason
for something in the template that would otherwise look arbitrary.

1. **The items are rendered twice.** Each copy slides by its own width and one gap, which is where
   the other copy began, so the loop has no seam. The second copy is `inert` and hidden from
   assistive technology, so a link is reached once and a name is read once.
2. **Each copy is at least as wide as the row.** Three logos spread across the belt. Without this
   they would pass in a clump with a gap behind them, and one logo would show an empty belt most
   of the time.
3. **Direction and play state are custom properties read inside the `animation` shorthand.** The
   shorthand resets `animation-direction` and `animation-play-state`. Set as utilities of their
   own, whether they applied depended on the order the stylesheet happened to emit them in.
4. **A marquee draws a pause control.** It is a checkbox, and the row reads it with `:has()`. The
   row also stops under the pointer and while anything inside it has focus.
5. **Several rows share one control.** An element carrying `data-marquee-group` holds one
   `<c-marquee.pause>` for every marquee inside it, and each marquee hides its own there.
6. **Under reduced motion there is one copy, still, wrapped and centred.** The pause control and
   the fade at the ends are not drawn.
7. **A logo is not lazily loaded.** An image that has not loaded has no width, so the second copy
   was narrower than the first until it scrolled into view, and the loop jumped.
8. **Tone and logo size are set on the block and read by the logos.** The block carries
   `data-logo-tone` and `--logo-size`. A slot's content cannot be handed an attribute, and twelve
   logos should not each repeat one.

## Why

Movement that starts by itself, runs for more than five seconds and sits beside other content
needs a way to pause, stop or hide it (WCAG 2.2.2, Level A). Stopping under the pointer serves a
mouse only. Stopping on focus serves a keyboard only when the row holds links. The control serves
everyone, and a checkbox gives it without a script.

[ADR 0004](0004-moving-backgrounds-are-css-only.md) accepted that the moving backgrounds have no
pause control. A background is decoration behind the copy. A marquee is content: the logos are
what the visitor is there to read.

A script would make a constant speed possible whatever the row holds, and would let the row be
dragged. Neither is worth being the first script a project has to load for this package
(`CONSTITUTION.md` Article XV).

## What it costs

- **`speed` sets how often the row comes round and not how fast it crosses the screen.** CSS
  cannot measure the row. A row holding more moves faster at the same number.
- **The page carries every item twice.** An `id` inside a marquee is duplicated.
- **`controls` can turn the control off.** A page that does so, and gives no other way to stop
  the row, fails the criterion above. The option says so where it is documented.
- **A browser without `:has()` or `inert` gets less.** The control does nothing without `:has()`,
  and without `inert` the second copy's links take focus. Both have been in every major browser
  since 2023.
