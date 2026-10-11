# ADR 0013 — A footer block is the footer element

**Status:** accepted

## Decision

Every footer block renders a `footer` element as its outer element, with the section shell inside
it. The rules that follow:

1. **Undeclared attributes reach the `footer`. `class` reaches the section inside it,** which is
   the surface: the element that carries the padding, the copy colour and the background layer.
2. **Columns of links are daisy-cotton's `<c-footer.nav>`,** placed in a `div` that carries
   daisyUI's `footer` class. No block uses daisy-cotton's `<c-footer>` itself.
3. **Links and social links are slots filled with daisy-cotton's link and button.** The package
   adds no component for either.
4. **The same slot names in every block:** the default slot for the links, `logo`, `social`,
   `legal` and `background`. A layout with something more adds a slot for it, as the banner does
   with `actions`.
5. **A block that asks for something ships no form.** The form goes in a slot whole.
6. **What the blocks share is two components,** `<c-footer.brand>` and `<c-footer.legal>`.

## Why

Every other block is a section, and a footer written the same way would be a `footer` inside a
`section`. HTML gives that element to the section and not to the page, so it stops being the
contentinfo landmark a screen reader offers as the end of the page. Putting the `footer` outside
keeps the landmark and still gets the section's width, background layer and `invert` for nothing.

daisy-cotton's `<c-footer>` renders a `footer` element too, and a footer may not contain another.
What the blocks need from daisyUI is not the element but the rule that stacks the links of each
group, and that rule follows the `footer` class wherever it is written. The groups themselves are
daisy-cotton's, per ADR 0007.

Splitting `class` from the other attributes is the cost. A surface colour on the outer `footer`
would work, but a padding or a copy colour passed the same way would lose to the section's own,
and a caller should not have to know which is which. One rule, that `class` styles the surface,
is the same thing every other block already says.

## Consequences

- The package relies on daisyUI's `footer` class from the project, which is in
  `HOST_PROVIDED_CLASSES`.
- A page author must place the block outside `main` and outside any sectioning element. The block
  cannot check that.
- The tag family `footer.*` sits beside daisy-cotton's `footer` and `footer.nav`, as `hero.*`
  already sits beside its `hero`. A later daisy-cotton component named `footer.brand` or
  `footer.legal` would be shadowed by whichever app is listed first.
