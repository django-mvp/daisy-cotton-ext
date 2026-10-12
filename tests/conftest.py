"""Shared fixtures for the test suite."""

from collections.abc import Callable, Iterator
from pathlib import Path

import pytest
from django.template import engines
from django_cotton.compiler_regex import CottonCompiler
from playwright.sync_api import Browser, sync_playwright


@pytest.fixture
def render() -> Callable[..., str]:
    def _render(markup: str, **context: object) -> str:
        compiled = CottonCompiler().process(markup)
        return engines["django"].from_string(compiled).render(context)

    return _render


@pytest.fixture(scope="session")
def browser() -> Iterator[Browser]:
    with sync_playwright() as playwright:
        if not Path(playwright.chromium.executable_path).exists():
            pytest.skip(
                "Chromium is not installed: run `uv run playwright install chromium`"
            )
        chromium = playwright.chromium.launch()
        yield chromium
        chromium.close()
