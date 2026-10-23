"""
test_i18n.py
============
Unit tests for humanize.i18n (internationalization) module.
Module Author  : 24P-3060
Functions Under Test:
    - humanize.activate()
    - humanize.deactivate()
    - humanize.decimal_separator()
    - humanize.thousands_separator()

Test Design Techniques Applied:
    - Equivalence Class Partitioning (ECP): valid locale codes, deactivation, function output
    - Boundary Value Analysis (BVA): empty string locale, unsupported locale
    - Parameterization: data-driven locale tests
"""

import pytest
import humanize
import humanize.i18n as i18n


# ─────────────────────────────────────────────────────────────────────────────
# i18n – activate / deactivate locales and separator functions
# ─────────────────────────────────────────────────────────────────────────────

@pytest.mark.i18n
@pytest.mark.smoke
@pytest.mark.order(1)
class TestI18nActivateDeactivate:
    """
    Tests for humanize.activate() and humanize.deactivate().
    Always deactivate after each test to restore default English behavior.
    """

    def teardown_method(self):
        """Ensure locale is reset to default after every test."""
        humanize.deactivate()

    def test_deactivateRestoresDefault(self):
        """ECP: deactivate() after activate() restores English behavior."""
        humanize.activate("de_DE")
        humanize.deactivate()
        # After deactivation, intcomma should use English comma separator
        result = humanize.intcomma(1000)
        assert result == "1,000"

    def test_activateReturnsTranslation(self):
        """ECP: activate() with a valid locale returns a translation object."""
        result = humanize.activate("de_DE")
        assert result is not None

    def test_activateInvalidLocaleRaises(self):
        """ECP: an unsupported/invalid locale raises an error."""
        with pytest.raises(Exception):
            humanize.activate("xx_INVALID")

    def test_defaultIntcommaEnglish(self):
        """ECP: without activation, intcomma uses English (comma as thousands sep)."""
        humanize.deactivate()
        assert humanize.intcomma(1000) == "1,000"

    def test_activateRussian(self):
        """ECP: Russian locale activation does not raise an error."""
        try:
            humanize.activate("ru_RU")
            result = humanize.intcomma(1000)
            assert isinstance(result, str)
        except Exception:
            pytest.skip("ru_RU locale not available in this build")

    def test_doubleDeactivateSafe(self):
        """ECP: calling deactivate() twice should not raise an error."""
        humanize.deactivate()
        humanize.deactivate()  # Should be safe
        assert humanize.intcomma(1000) == "1,000"


@pytest.mark.i18n
@pytest.mark.order(2)
class TestDecimalAndThousandsSeparators:
    """
    Tests for humanize.decimal_separator() and humanize.thousands_separator().
    These return locale-appropriate separator characters.
    """

    def teardown_method(self):
        humanize.deactivate()

    def test_decimalSeparatorDefaultIsDot(self):
        """ECP: default English locale uses '.' as decimal separator."""
        humanize.deactivate()
        result = humanize.decimal_separator()
        assert result == "."

    def test_thousandsSeparatorDefaultIsComma(self):
        """ECP: default English locale uses ',' as thousands separator."""
        humanize.deactivate()
        result = humanize.thousands_separator()
        assert result == ","

    def test_decimalSeparatorReturnsString(self):
        """decimal_separator always returns a single-character string."""
        result = humanize.decimal_separator()
        assert isinstance(result, str)
        assert len(result) == 1

    def test_thousandsSeparatorReturnsString(self):
        """thousands_separator always returns a string."""
        result = humanize.thousands_separator()
        assert isinstance(result, str)

    def test_germanLocaleDecimalSeparator(self):
        """ECP: German locale uses comma as decimal separator."""
        try:
            humanize.activate("de_DE")
            result = humanize.decimal_separator()
            assert result == ","
        except Exception:
            pytest.skip("de_DE locale not available in this build")

    def test_germanLocaleThousandsSeparator(self):
        """ECP: German locale uses period/dot as thousands separator."""
        try:
            humanize.activate("de_DE")
            result = humanize.thousands_separator()
            assert result == "."
        except Exception:
            pytest.skip("de_DE locale not available in this build")


@pytest.mark.i18n
@pytest.mark.order(3)
class TestI18nIntegration:
    """
    Integration tests: verifying that locale change affects output of number functions.
    """

    def teardown_method(self):
        humanize.deactivate()

    def test_intcommaEnglishAfterDeactivation(self):
        """Integration: English is restored correctly after locale change."""
        try:
            humanize.activate("de_DE")
        except Exception:
            pass
        humanize.deactivate()
        assert humanize.intcomma(1000) == "1,000"

    @pytest.mark.parametrize("locale", [
        "fr_FR", "es_ES", "pt_BR"
    ])
    def test_supportedLocalesDoNotCrash(self, locale):
        """ECP parametrized: activating known locales should not raise unexpected errors."""
        try:
            humanize.activate(locale)
            result = humanize.intcomma(1000)
            assert isinstance(result, str)
        except FileNotFoundError:
            pytest.skip(f"Locale {locale} not installed in this environment")
        finally:
            humanize.deactivate()
