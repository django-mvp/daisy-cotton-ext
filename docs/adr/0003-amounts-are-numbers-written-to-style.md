# ADR 0003 — An amount is a number, written to the element's style

**Status:** accepted

## Decision

An option that sets an amount takes a number, and any number works: speed, intensity, opacity, and
a size where fine control is the point, such as how far apart a grid's rules sit. An option that
picks from a designed scale keeps its names: a font size, a button size, a block's `size`.

The number reaches the page on the element's `style` attribute, either as a custom property the
stylesheet reads (`--grid-size: 3.5rem`) or as one plain declaration (`opacity: 0.2`). Nothing else
is written to `style`, with the one exception below. Anything longer is a class.

**The exception is a logo's image address.** `<c-logos.logo>` writes `--logo-src: url("…")` so that
the `ink` tone can paint the text colour through the image as a mask. A mask has to be named in
CSS, and no class can carry an address the template author supplies. The address goes through
`iriencode` inside a double-quoted `url()`. The filter percent-encodes a double quote, a backslash
and a line break, so the address cannot end its own string. Two fixed values are written beside
it, `--logo-ink` and `--logo-seen`, which switch the paint on and the image off.

Every value goes through `floatformat:'-3u'|default:'<default>'` on its way in. The filter emits a
number or nothing, and `default` fills the gap, so a value that is not a number renders the
component's default.

## Why

The backgrounds first took names: `intensity="faint"`, `"soft"` or `"bold"`, each mapped to a
utility class. Three steps were enough for a glow. They were not enough for movement, where the
difference between a background that is pleasant and one that is distracting sits between any two
steps a name can offer, and the author is the only one who can find it.

The alternative that keeps classes is a fixed list of numbers, each built into the stylesheet as
its own rule. It reads as a number and behaves as a name: the value the author wants is not on the
list, and every value on the list costs bytes in every install.

Until now no component wrote a `style` attribute at all, and a test said so. The intent was to keep
styling in classes, where a host's content security policy cannot block it and where a URL or a
long declaration cannot be smuggled in. A single number does not carry those risks once it is
forced to be a number, which is what `floatformat` does. `u` keeps a locale from writing a decimal
comma into CSS.

## Consequences

- A page served under a content security policy that forbids inline styles ignores the attribute.
  Each component therefore states its default twice: in `<c-vars>` and as the fallback of the
  `var()` or the declaration it replaces. Such a page gets working backgrounds at their defaults.
- A name from the earlier releases is no longer recognised. `intensity="bold"` renders the default.
- The same page shows an `ink` logo as the file itself. The paint, the mask and the hiding of the
  image all hang on values in the attribute, so they are lost together and never in part.
  `tests/test_logos_blocks.py` holds the address inside its quotes.
- `inf` and `nan` pass the filter as those words. A browser discards the declaration, which leaves
  the default, and neither can carry a second declaration.
- `tests/test_background_blocks.py` holds every number option to this: the number arrives, a
  non-number falls back, and a value carrying a declaration never reaches the attribute.
