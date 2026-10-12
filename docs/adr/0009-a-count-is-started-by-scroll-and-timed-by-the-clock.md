# ADR 0009 — A count is started by scroll and timed by the clock

**Status:** accepted

## Decision

`<c-stats.count>` counts up once, in CSS, with no script, in three parts:

1. **The scroll position throws a switch.** A scroll-driven animation on the figure sets a custom
   property, `--dce-seen`, from 0 to 1 as the figure comes into view. Scrolling back until the
   figure is below the window sets it to 0 again, because a scroll-driven animation runs both
   ways.
2. **The switch starts a transition.** A style query on that property sets `--dce-count`, a
   custom property registered as a whole number, to the number asked for. A transition on
   `--dce-count` does the counting, and a CSS counter writes its value out.
3. **The count does not go back.** While the switch is off, the transition on `--dce-count` has
   a delay that never ends. So when the switch goes off, the move back to 0 is set up and never
   starts, and the figure keeps the number it has. When the switch comes on again there is
   nothing left to count.

The finished number is in the markup as ordinary text. Where the browser supports all of this and
the visitor has not asked for reduced motion, that text is hidden visually and the counter is
shown in its place. Everywhere else the text is what is seen. A screen reader is always given the
text and never the counter.

## Why

The reveals tie their movement directly to the scroll position
([ADR 0006](0006-reveals-follow-the-scroll-position.md)). A count cannot do that. A figure that
stops halfway up the screen would stop halfway through its count and show 23 where the truth is
31. A half-faded card is harmless. A wrong number is not.

Running the count on the clock means it always finishes on the number given, however far the page
is scrolled.

A figure that has been read should not go back to 0. A visitor scrolling up the page would
otherwise watch every number run again, and a number that keeps moving is harder to trust than
one that holds still. The switch cannot hold itself on, since the scroll position that turns it
on also turns it off, so the holding is done by the transition it starts. Starting it from the scroll position keeps it script-free, like every other movement
in the package ([ADR 0004](0004-moving-backgrounds-are-css-only.md)).

## Consequences

- **Whole numbers only, with no separators.** A CSS counter cannot format a number. Text before
  and after the number carries a currency sign, a unit or the decimals.
- **"In view" is measured against the nearest scrolling box.** daisyUI's `stats` row is one, so a
  counting stat inside it is always in view and counts once as the page loads. `<c-stats.band>`
  and a plain grid are not, and a count there waits for the visitor.
- **A browser without scroll-driven animation or style queries shows the finished number.** That
  is a complete result, not a degraded one.
- **A count interrupted part-way waits where it stopped.** If the figure leaves the bottom of the
  window before it has finished, it holds that number out of sight and finishes when it is next
  in view.
- **Reloading the page is the only way to see a count twice.**
- The stylesheet carries an `@property` rule and the `dce-seen` keyframes for this, beside the
  other movement it defines.
