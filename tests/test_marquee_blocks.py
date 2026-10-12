"""The marquee: a row of anything that travels across the page without end.

The row is written out twice so the loop has no seam, and the second copy is
taken out of the reach of a keyboard and a screen reader. The movement is CSS
alone. A checkbox is the pause control, and the stylesheet reads whether it is
ticked.
"""

import re

ITEM = '<a id="inside" href="#">Northwind</a>'


def marquee(attributes: str = "", inside: str = ITEM) -> str:
    """Return markup for a marquee."""
    return f"<c-marquee {attributes}>{inside}</c-marquee>"


def style_value(html: str, name: str) -> str:
    """Return the value the first `style` attribute gives a custom property."""
    found = re.search(rf'style="[^"]*?{re.escape(name)}: ([^;"]*)', html)
    assert found is not None, f"no {name} in a style attribute"
    return found.group(1)


class TestTheRow:
    def test_the_items_are_written_out_twice(self, render) -> None:
        assert render(marquee()).count('id="inside"') == 2

    def test_the_second_copy_is_out_of_reach(self, render) -> None:
        html = render(marquee())

        copy = re.search(
            r"<div aria-hidden=\"true\"\s+inert\b[^>]*>(.*?)</div>", html, re.S
        )
        assert copy is not None
        assert 'id="inside"' in copy.group(1)

    def test_the_first_copy_is_within_reach(self, render) -> None:
        html = render(marquee())

        before_the_copy = html.split("inert")[0]
        assert 'id="inside"' in before_the_copy

    def test_the_outer_element_carries_the_hook_the_stylesheet_reads(
        self, render
    ) -> None:
        assert re.match(r"\s*<div data-marquee\b", render(marquee())) is not None

    def test_extra_classes_and_attributes_reach_the_outer_element(self, render) -> None:
        html = render(marquee('id="belt" class="mt-8"'))

        assert re.match(r'\s*<div data-marquee[^>]*class="[^"]*\bmt-8\b', html)
        assert re.match(r'\s*<div data-marquee[^>]*\bid="belt"', html)


class TestSpeed:
    def test_a_number_reaches_the_style(self, render) -> None:
        assert (
            float(style_value(render(marquee('speed="2.5"')), "--marquee-speed")) == 2.5
        )

    def test_the_default_is_one(self, render) -> None:
        assert style_value(render(marquee()), "--marquee-speed") == "1"

    def test_a_value_that_is_not_a_number_falls_back(self, render) -> None:
        assert style_value(render(marquee('speed="fast"')), "--marquee-speed") == "1"

    def test_a_value_carrying_a_declaration_cannot_reach_the_style(
        self, render
    ) -> None:
        html = render(marquee('speed="1; background: red"'))

        assert "background: red" not in html


class TestDirection:
    def test_the_row_travels_left_unless_told_otherwise(self, render) -> None:
        assert "--marquee-direction:reverse" not in render(marquee())

    def test_reverse_turns_it_round(self, render) -> None:
        assert "dce:[--marquee-direction:reverse]" in render(marquee("reverse"))


class TestThePauseControl:
    def test_it_is_a_checkbox_the_stylesheet_can_find(self, render) -> None:
        html = render(marquee())

        assert (
            len(re.findall(r'<input type="checkbox"\s+data-marquee-pause', html)) == 1
        )

    def test_it_has_a_name_without_being_given_one(self, render) -> None:
        html = render(marquee())

        assert re.search(r'data-marquee-pause\s+aria-label="[^"]+"', html) is not None

    def test_it_takes_the_name_it_is_given(self, render) -> None:
        html = render(marquee('pause="Stop the sponsors"'))

        assert 'aria-label="Stop the sponsors"' in html

    def test_its_name_is_escaped(self, render) -> None:
        html = render('<c-marquee :pause="name">x</c-marquee>', name='"><script>')

        assert "<script>" not in html

    def test_it_can_be_left_out(self, render) -> None:
        assert "<input" not in render(marquee(':controls="False"'))

    def test_it_gives_way_to_a_groups_control(self, render) -> None:
        html = render(marquee())

        assert re.search(r'<label class="[^"]*dce:in-data-marquee-group:hidden', html)


class TestThePauseControlOnItsOwn:
    def test_it_is_not_hidden_inside_a_group(self, render) -> None:
        html = render("<c-marquee.pause />")

        assert "<input" in html
        assert "in-data-marquee-group:hidden" not in html

    def test_extra_classes_and_attributes_reach_the_control(self, render) -> None:
        html = render('<c-marquee.pause id="stop" class="mt-2" />')

        assert re.match(r'\s*<label class="[^"]*\bmt-2\b', html) is not None
        assert re.match(r'\s*<label[^>]*\bid="stop"', html) is not None
