# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest

TEST_PO_DE = """\
# Translation of testdomain.pot to German
msgid ""
msgstr ""
"Project-Id-Version: Plone"
"POT-Creation-Date: YEAR-MO-DA HO:MI +ZONE"
"PO-Revision-Date: 2016-10-22 16:41-0500"
"Last-Translator: Foo Bar <foo.bar@plone.org>"
"Language-Team: German <i18n-de@plone.org>"
"MIME-Version: 1.0"
"Content-Type: text/plain; charset=UTF-8"
"Content-Transfer-Encoding: 8bit"
"Plural-Forms: nplurals=1; plural=0;"
"Language-Code: de"
"Language-Name: Deutsch"
"Preferred-Encodings: utf-8 latin1"
"Domain: plone"
"X-Is-Fallback-For: de-at de-li de-lu de-ch de-de"
"Language: de"
"X-Generator: Poedit 1.5.4"

#: testdomain/testdomain/interfaces.py:97
msgid "Watch Columbo"
msgstr "Columbo schaun"

#: testdomain/testdomain/interfaces.py:109
msgid "days_and_hours"
msgstr "$d Tage und $h Stunden"
"""


class TestTranslationDomain(unittest.TestCase):
    """Test that collective.zanata is properly installed."""

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def setUp(self):
        from collective.zanata.storage import I18NDomainStorage
        self.domain_storage = I18NDomainStorage('testdomain')
        zl = self.domain_storage.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

    def test_create(self):
        from collective.zanata.translationdomain import LocalTranslationDomain
        ltd = LocalTranslationDomain(self.domain_storage.name)
        self.assertEqual(ltd.domain, self.domain_storage.name)

    def test_add_catalog(self):
        from collective.zanata.translationdomain import LocalTranslationDomain
        ltd = LocalTranslationDomain(self.domain_storage.name)
        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lmc = LocalGettextMessageCatalog(self.domain_storage.language('de'))
        ltd.addCatalog(lmc)
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )
        self.assertEqual(
            ltd.translate(
                'days_and_hours',
                target_language='de',
                mapping={'d': '10', 'h': 13}
            ),
            u'10 Tage und 13 Stunden',
        )