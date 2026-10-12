"""The logos family: sponsors and partners on a moving belt.

Five blocks lay out one or more marquees of logos, and three parts go inside
them. A block sets the tone and the size of its logos once, on an element the
logos read. A block with several rows draws one pause control for all of them.
"""

import re

import pytest

BLOCKS = [
    "c-logos.belt",
    "c-logos.rows",
    "c-logos.inline",
    "c-logos.tiers",
    "c-logos.split",
]

# The blocks that take a row of logos directly, and wrap it in a marquee.
ONE_ROW = ["c-logos.belt", "c-logos.inline"]

# The blocks whose rows are marquees or tiers the template author writes.
SEVERAL_ROWS = ["c-logos.rows", "c-logos.tiers", "c-logos.split"]

# The blocks that open with the shared heading.
WITH_HEADING = ["c-logos.belt", "c-logos.rows", "c-logos.tiers", "c-logos.split"]

LOGO = '<c-logos.logo src="/static/northwind.svg" name="Northwind" />'
ROW = f"<c-marquee>{LOGO}</c-marquee>"


def block(tag: str, attributes: str = "", inside: str | None = None) -> str:
    """Return markup for a logos block holding one row."""
    if inside is None:
        inside = LOGO if tag in ONE_ROW else ROW
    return f"<{tag} {attributes}>{inside}</{tag}>"


def controls_drawn(html: str) -> list[str]:
    """Return the class of each pause control that is not giving way to a group's."""
    controls = re.findall(r'<label class="([^"]*)"', html)
    if re.search(r"<div data-marquee-group\b", html) is None:
        return controls
    return [c for c in controls if "in-data-marquee-group:hidden" not in c]


def logo(attributes: str = "") -> str:
    """Return markup for one logo."""
    return f'<c-logos.logo src="/static/northwind.svg" name="Northwind" {attributes} />'


def tile(attributes: str = "") -> str:
    """Return markup for one logo tile."""
    return f'<c-logos.tile src="/static/northwind.svg" name="Northwind" {attributes} />'


class TestEveryBlock:
    @pytest.mark.parametrize("tag", BLOCKS)
    def test_it_is_one_section(self, render, tag) -> None:
        html = render(block(tag))

        assert re.match(r"\s*<section\b", html) is not None
        assert html.count("<section") == 1

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_an_undeclared_attribute_reaches_the_section(self, render, tag) -> None:
        html = render(block(tag, 'id="sponsors"'))

        assert re.match(r'\s*<section[^>]*\bid="sponsors"', html) is not None

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_extra_classes_reach_the_section(self, render, tag) -> None:
        html = render(block(tag, 'class="bg-base-200"'))

        assert re.match(r'\s*<section[^>]*class="[^"]*\bbg-base-200\b', html)

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_the_logos_are_rendered(self, render, tag) -> None:
        assert 'alt="Northwind"' in render(block(tag))

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_the_tone_is_set_once_for_every_logo_inside(self, render, tag) -> None:
        html = render(block(tag, 'tone="ink"'))

        assert html.count('data-logo-tone="ink"') == 1

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_there_is_one_pause_control_however_many_rows(self, render, tag) -> None:
        rows = LOGO if tag in ONE_ROW else ROW + ROW + ROW
        html = render(block(tag, inside=rows))

        assert len(controls_drawn(html)) == 1

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_the_pause_control_takes_the_name_it_is_given(self, render, tag) -> None:
        html = render(block(tag, 'pause="Stop the sponsors"'))

        assert 'aria-label="Stop the sponsors"' in html

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_the_pause_control_can_be_left_out(self, render, tag) -> None:
        html = render(block(tag, ':controls="False"'))

        assert controls_drawn(html) == []


class TestSeveralRows:
    @pytest.mark.parametrize("tag", SEVERAL_ROWS)
    def test_the_rows_are_one_group_for_the_pause_control(self, render, tag) -> None:
        html = render(block(tag, inside=ROW + ROW))

        assert len(re.findall(r"<div data-marquee-group\b", html)) == 1
        group = re.split(r"<div data-marquee-group\b", html)[1]
        assert len(re.findall(r"<div data-marquee\s", group)) == 2

    @pytest.mark.parametrize("tag", ONE_ROW)
    def test_a_single_row_is_no_group(self, render, tag) -> None:
        assert re.search(r"<div data-marquee-group\b", render(block(tag))) is None


class TestTheHeading:
    @pytest.mark.parametrize("tag", WITH_HEADING)
    def test_a_title_is_a_heading_at_the_level_asked_for(self, render, tag) -> None:
        html = render(block(tag, 'title="Our sponsors" level="3"'))

        assert re.search(r"<h3\b[^>]*>Our sponsors</h3>", html) is not None

    @pytest.mark.parametrize("tag", ["c-logos.belt", "c-logos.rows", "c-logos.tiers"])
    def test_no_heading_is_drawn_when_none_is_given(self, render, tag) -> None:
        html = render(block(tag))

        assert re.search(r"<h[1-6]\b", html) is None


class TestBelt:
    def test_the_speed_reaches_the_marquee(self, render) -> None:
        html = render(block("c-logos.belt", 'speed="0.5"'))

        assert "--marquee-speed: 0.5" in html

    def test_reverse_reaches_the_marquee(self, render) -> None:
        assert "--marquee-direction:reverse" not in render(block("c-logos.belt"))
        assert "dce:[--marquee-direction:reverse]" in render(
            block("c-logos.belt", "reverse")
        )

    def test_full_runs_the_belt_to_the_edges(self, render) -> None:
        assert "dce:max-w-none" not in render(block("c-logos.belt"))
        assert "dce:max-w-none" in render(block("c-logos.belt", 'container="full"'))


class TestInline:
    def test_it_has_words_beside_the_logos_without_being_given_any(
        self, render
    ) -> None:
        html = render(block("c-logos.inline"))

        assert re.search(r"<p\b[^>]*>[^<]+</p>", html) is not None

    def test_it_takes_the_words_it_is_given(self, render) -> None:
        html = render(block("c-logos.inline", 'label="Funded by"'))

        assert re.search(r"<p\b[^>]*>Funded by</p>", html) is not None

    def test_the_logos_are_muted_unless_told_otherwise(self, render) -> None:
        assert 'data-logo-tone="muted"' in render(block("c-logos.inline"))


class TestTiers:
    TIER = f'<c-logos.tier label="Gold" note="Funds a maintainer">{LOGO}</c-logos.tier>'

    def test_a_tier_names_its_level(self, render) -> None:
        html = render(block("c-logos.tiers", inside=self.TIER))

        assert re.search(r"<p\b[^>]*>Gold</p>", html) is not None
        assert "Funds a maintainer" in html

    def test_a_tier_without_a_note_leaves_nothing_behind(self, render) -> None:
        html = render(f'<c-logos.tier label="Gold">{LOGO}</c-logos.tier>')

        assert len(re.findall(r"<p\b", html)) == 1

    def test_a_tier_sets_the_size_of_its_own_logos(self, render) -> None:
        html = render(
            f'<c-logos.tier label="Gold" logo-size="lg">{LOGO}</c-logos.tier>'
        )

        assert "dce:[--logo-size:3rem]" in html

    def test_a_tiers_logos_travel_in_a_marquee(self, render) -> None:
        html = render(f'<c-logos.tier label="Gold" speed="0.5">{LOGO}</c-logos.tier>')

        assert "--marquee-speed: 0.5" in html
        assert html.count('alt="Northwind"') == 2

    def test_a_tier_passes_classes_and_attributes_to_its_row(self, render) -> None:
        html = render(f'<c-logos.tier id="gold" class="mt-8">{LOGO}</c-logos.tier>')

        assert re.match(r'\s*<div class="[^"]*\bmt-8\b', html) is not None
        assert re.match(r'\s*<div[^>]*\bid="gold"', html) is not None

    def test_the_actions_sit_outside_the_moving_rows(self, render) -> None:
        action = '<c-slot name="actions"><a id="join" href="#">Join</a></c-slot>'
        html = render(block("c-logos.tiers", inside=self.TIER + action))

        assert html.count('id="join"') == 1


class TestSplit:
    def test_the_actions_are_rendered_once(self, render) -> None:
        action = '<c-slot name="actions"><a id="join" href="#">Join</a></c-slot>'
        html = render(block("c-logos.split", 'title="Join us"', inside=ROW + action))

        assert html.count('id="join"') == 1

    def test_no_actions_leaves_nothing_behind(self, render) -> None:
        with_actions = render(
            block(
                "c-logos.split",
                inside=ROW + '<c-slot name="actions"><a href="#">Join</a></c-slot>',
            )
        )
        without = render(block("c-logos.split"))

        assert without.count("<div") == with_actions.count("<div") - 1

    def test_the_words_and_the_rows_are_two_columns(self, render) -> None:
        assert (
            len(re.findall(r"<div data-section-col\b", render(block("c-logos.split"))))
            == 2
        )


class TestLogo:
    def test_the_name_is_the_images_text(self, render) -> None:
        assert 'alt="Northwind"' in render(logo())

    def test_the_name_is_escaped(self, render) -> None:
        html = render(
            '<c-logos.logo src="/a.svg" :name="name" />', name='"><script>alert(1)'
        )

        assert "<script>" not in html

    def test_it_is_a_link_when_given_somewhere_to_go(self, render) -> None:
        html = render(logo('href="https://example.com"'))

        assert re.match(r'\s*<a href="https://example.com"', html) is not None

    def test_it_is_not_a_link_otherwise(self, render) -> None:
        html = render(logo())

        assert "<a" not in html
        assert re.match(r"\s*<span\b", html) is not None

    def test_it_takes_its_tone_from_around_it_unless_given_one(self, render) -> None:
        assert "data-logo-tone" not in render(logo())
        assert 'data-logo-tone="ink"' in render(logo('tone="ink"'))

    def test_it_takes_its_size_from_around_it_unless_given_one(self, render) -> None:
        assert "dce:[--logo-size:" not in render(logo())
        assert "dce:[--logo-size:4rem]" in render(logo('size="xl"'))

    def test_the_images_address_reaches_the_style_for_the_ink_tone(
        self, render
    ) -> None:
        html = render(logo())

        assert '--logo-src: url("/static/northwind.svg")' in html

    def test_an_address_cannot_close_its_own_quotes(self, render) -> None:
        html = render(
            '<c-logos.logo :src="src" name="x" />',
            src='/a.svg"); background: url("//evil.example/x',
        )

        style = re.search(r"style='([^']*)'", html)
        assert style is not None
        assert style.group(1).count('"') == 2
        assert "background:" not in style.group(1).replace("%20", " ").split('")')[1]

    def test_extra_classes_and_attributes_reach_the_outer_element(self, render) -> None:
        html = render(logo('id="first" class="mx-4"'))

        assert re.search(r'<span\s+class="[^"]*\bmx-4\b', html) is not None
        assert re.search(r'<span[^>]*\bid="first"', html) is not None


class TestTile:
    def test_the_name_is_written_out_and_the_image_says_nothing(self, render) -> None:
        html = render(tile())

        assert re.search(r"<p\b[^>]*>Northwind</p>", html) is not None
        assert 'alt=""' in html

    def test_the_name_is_the_link_when_given_somewhere_to_go(self, render) -> None:
        html = render(tile('href="https://example.com"'))

        assert re.search(r'<a href="https://example.com"[^>]*>Northwind</a>', html)
        assert html.count("<a ") == 1

    def test_it_is_not_a_link_otherwise(self, render) -> None:
        assert "<a " not in render(tile())

    def test_a_note_is_shown_under_the_name(self, render) -> None:
        assert "Founding sponsor" in render(tile('note="Founding sponsor"'))

    def test_no_note_leaves_nothing_behind(self, render) -> None:
        assert len(re.findall(r"<p\b", render(tile()))) == 1

    def test_it_is_a_daisyui_card(self, render) -> None:
        assert re.match(r'\s*<div class="card\b', render(tile())) is not None

    def test_extra_classes_and_attributes_reach_the_card(self, render) -> None:
        html = render(tile('id="first" class="mx-4"'))

        assert re.match(r'\s*<div class="card[^"]*\bmx-4\b', html) is not None
        assert re.match(r'\s*<div[^>]*\bid="first"', html) is not None
