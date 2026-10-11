"""The footer family: the end of a page, and the two parts the blocks share.

A footer block is the page's `footer` element with a section inside it, so it is
the contentinfo landmark whatever it holds. The link columns are daisy-cotton's
own `c-footer.nav`, inside an element carrying daisyUI's `footer` class. Every
part of a footer is optional, and a part left out leaves nothing behind.
"""

import re

import pytest

BLOCKS = ["c-footer.columns", "c-footer.centred", "c-footer.slim", "c-footer.banner"]

# The blocks that close on the copyright line under a rule, with a `legal` slot.
WITH_LEGAL_SLOT = ["c-footer.columns", "c-footer.centred", "c-footer.banner"]

# The blocks that take a background.
WITH_BACKGROUND = WITH_LEGAL_SLOT

# The blocks whose links are columns of footer.nav groups.
WITH_COLUMNS = ["c-footer.columns", "c-footer.banner"]

PARTS = ["c-footer.brand", "c-footer.legal"]

LINK = '<a id="inside" href="#">Pricing</a>'


def slot(name: str, markup: str) -> str:
    """Return markup filling a named slot."""
    return f'<c-slot name="{name}">{markup}</c-slot>'


def footer(tag: str, attributes: str = "", inside: str = LINK) -> str:
    """Return markup for a footer block or part."""
    return f"<{tag} {attributes}>{inside}</{tag}>"


class TestEveryFooterIsTheLandmark:
    @pytest.mark.parametrize("tag", BLOCKS)
    def test_the_outer_element_is_the_only_footer(self, render, tag) -> None:
        html = render(footer(tag))

        assert re.match(r"\s*<footer\b", html) is not None
        assert html.count("<footer") == 1

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_an_undeclared_attribute_reaches_the_footer(self, render, tag) -> None:
        html = render(footer(tag, 'id="end"'))

        assert re.match(r'\s*<footer[^>]*\bid="end"', html) is not None

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_extra_classes_reach_the_surface(self, render, tag) -> None:
        html = render(footer(tag, 'class="bg-base-200"'))

        assert re.search(r'<section[^>]*class="[^"]*\bbg-base-200\b', html) is not None

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_invert_sets_light_copy(self, render, tag) -> None:
        assert "dce:text-neutral-content" not in render(footer(tag))
        assert "dce:text-neutral-content" in render(footer(tag, "invert"))

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_wide_holds_the_content_wider(self, render, tag) -> None:
        assert "dce:max-w-6xl" in render(footer(tag))
        assert "dce:max-w-7xl" in render(footer(tag, 'container="wide"'))

    @pytest.mark.parametrize("tag", WITH_BACKGROUND)
    def test_a_background_goes_in_a_hidden_layer(self, render, tag) -> None:
        html = render(footer(tag, inside=slot("background", '<i id="bg"></i>')))

        assert re.search(r'<div aria-hidden="true"[^>]*>\s*<i id="bg">', html)

    @pytest.mark.parametrize("tag", [*BLOCKS, *PARTS])
    def test_the_links_are_rendered(self, render, tag) -> None:
        assert 'id="inside"' in render(footer(tag))

    @pytest.mark.parametrize("tag", PARTS)
    def test_a_part_passes_classes_and_attributes_to_its_wrapper(
        self, render, tag
    ) -> None:
        html = render(footer(tag, 'id="part" class="mt-8"'))

        assert re.match(r'\s*<div[^>]*class="[^"]*\bmt-8\b', html) is not None
        assert re.match(r'\s*<div[^>]*\bid="part"', html) is not None


class TestTheLinks:
    @pytest.mark.parametrize("tag", WITH_COLUMNS)
    def test_columns_sit_in_a_daisyui_footer(self, render, tag) -> None:
        html = render(footer(tag))

        assert re.search(r'<div class="footer\b[^"]*">\s*<a id="inside"', html)

    @pytest.mark.parametrize("tag", ["c-footer.centred", "c-footer.slim"])
    def test_a_row_of_links_is_a_named_navigation(self, render, tag) -> None:
        html = render(footer(tag))

        assert re.search(r'<nav aria-label="Footer"[^>]*>\s*<a id="inside"', html)

    @pytest.mark.parametrize("tag", ["c-footer.centred", "c-footer.slim"])
    def test_label_renames_the_navigation(self, render, tag) -> None:
        html = render(footer(tag, 'label="Site"'))

        assert '<nav aria-label="Site"' in html

    @pytest.mark.parametrize(
        "tag",
        ["c-footer.centred", "c-footer.slim", "c-footer.banner", "c-footer.legal"],
    )
    def test_no_links_means_no_container_for_them(self, render, tag) -> None:
        html = render(footer(tag, 'notice="© Meridian"', inside=""))

        assert "<nav" not in html
        assert 'class="footer' not in html


class TestTheBrand:
    @pytest.mark.parametrize("tag", ["c-footer.columns", "c-footer.centred"])
    def test_the_logo_and_tagline_are_shown(self, render, tag) -> None:
        html = render(
            footer(
                tag, 'tagline="Ships daily"', LINK + slot("logo", '<b id="logo"></b>')
            )
        )

        assert html.count('id="logo"') == 1
        assert re.search(r"<p[^>]*>Ships daily</p>", html) is not None

    @pytest.mark.parametrize("tag", BLOCKS)
    def test_the_social_links_are_shown(self, render, tag) -> None:
        html = render(footer(tag, inside=LINK + slot("social", '<a id="social"></a>')))

        assert html.count('id="social"') == 1

    @pytest.mark.parametrize("tag", ["c-footer.slim", "c-footer.banner"])
    def test_the_logo_sits_on_the_copyright_line(self, render, tag) -> None:
        html = render(
            footer(tag, 'notice="© Meridian"', slot("logo", '<b id="logo"></b>'))
        )

        assert re.search(r'<b id="logo"></b>\s*<p>© Meridian</p>', html) is not None

    def test_columns_with_no_brand_have_no_brand_corner(self, render) -> None:
        with_brand = render(footer("c-footer.columns", 'tagline="Ships daily"'))
        without = render(footer("c-footer.columns"))

        assert "dce:lg:col-span-2" in with_brand
        assert "dce:lg:col-span-2" not in without

    def test_a_brand_with_nothing_in_it_is_an_empty_wrapper(self, render) -> None:
        html = render("<c-footer.brand />")

        assert re.fullmatch(r"\s*<div[^>]*>\s*</div>\s*", html) is not None

    def test_centre_stacks_the_brand_on_the_centre_line(self, render) -> None:
        html = render('<c-footer.brand align="centre" tagline="Ships daily" />')

        assert "dce:items-center" in html


class TestTheCopyrightLine:
    @pytest.mark.parametrize("tag", [*BLOCKS, "c-footer.legal"])
    def test_the_notice_is_shown(self, render, tag) -> None:
        html = render(footer(tag, 'notice="© Meridian"'))

        assert "<p>© Meridian</p>" in html

    @pytest.mark.parametrize("tag", WITH_LEGAL_SLOT)
    def test_the_small_links_are_a_navigation_of_their_own(self, render, tag) -> None:
        html = render(footer(tag, inside=LINK + slot("legal", '<a id="terms"></a>')))

        assert re.search(r'<nav aria-label="Legal"[^>]*>\s*<a id="terms">', html)

    @pytest.mark.parametrize("tag", ["c-footer.columns", "c-footer.centred"])
    def test_no_notice_and_no_small_links_means_no_line(self, render, tag) -> None:
        html = render(footer(tag))

        assert "dce:border-t" not in html
        assert 'aria-label="Legal"' not in html

    @pytest.mark.parametrize("tag", WITH_LEGAL_SLOT)
    def test_the_line_is_ruled_off_from_what_is_above_it(self, render, tag) -> None:
        html = render(footer(tag, 'notice="© Meridian"'))

        assert re.search(
            r'<div class="[^"]*\bdce:border-t\b[^"]*"[^>]*>\s*<div[^>]*>\s*'
            r"<p>© Meridian</p>",
            html,
        )

    def test_the_part_draws_its_rule_only_when_asked(self, render) -> None:
        assert "dce:border-t" not in render('<c-footer.legal notice="© Meridian" />')
        assert "dce:border-t" in render(
            '<c-footer.legal divided notice="© Meridian" />'
        )

    def test_the_part_names_its_links(self, render) -> None:
        html = render(footer("c-footer.legal", 'label="Small print"'))

        assert re.search(r'<nav aria-label="Small print"[^>]*>\s*<a id="inside"', html)

    def test_the_part_puts_its_ends_around_the_notice_and_links(self, render) -> None:
        html = render(
            footer(
                "c-footer.legal",
                'notice="© Meridian"',
                LINK
                + slot("start", '<b id="start"></b>')
                + slot("end", '<b id="end"></b>'),
            )
        )

        assert re.search(
            r'id="start".*© Meridian.*id="inside".*id="end"', html, re.DOTALL
        )


class TestTheBanner:
    def test_the_title_is_a_second_level_heading(self, render) -> None:
        html = render('<c-footer.banner title="Stay in touch" />')

        assert re.search(r"<h2[^>]*>Stay in touch</h2>", html) is not None

    def test_level_changes_the_heading_element(self, render) -> None:
        html = render('<c-footer.banner title="Stay in touch" level="3" />')

        assert re.search(r"<h3[^>]*>Stay in touch</h3>", html) is not None

    def test_a_title_slot_carries_markup(self, render) -> None:
        html = render(
            footer("c-footer.banner", inside=slot("title", "Stay <em>in</em>"))
        )

        assert re.search(r"<h2[^>]*>Stay <em>in</em></h2>", html) is not None

    def test_no_title_means_no_heading(self, render) -> None:
        html = render('<c-footer.banner lead="Once a month." />')

        assert "<h2" not in html
        assert re.search(r"<p[^>]*>Once a month.</p>", html) is not None

    def test_the_actions_are_whatever_the_page_gives(self, render) -> None:
        html = render(
            footer(
                "c-footer.banner",
                'title="Stay in touch"',
                slot("actions", '<form id="signup"></form>'),
            )
        )

        assert html.count('<form id="signup">') == 1

    def test_a_banner_alone_has_no_copyright_line(self, render) -> None:
        html = render('<c-footer.banner title="Stay in touch" />')

        assert "dce:border-t" not in html
