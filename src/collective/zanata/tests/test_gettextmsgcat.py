# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.tests.data import TEST_PO_DE
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestTranslationDomain(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def test_empty_language(self):
        # prepare a storage
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zd.language('de')

        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        with self.assertRaises(ValueError):
            LocalGettextMessageCatalog(zd.language('de'))

    def test_filled_identifer(self):
        # prepare a storage
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lm = LocalGettextMessageCatalog(zl)
        self.assertEqual(lm.getIdentifier(), 'collective.zanata/testdomain/de')

    def test_filled_compiled(self):
        # prepare a storage
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lm = LocalGettextMessageCatalog(zl)
        mo = lm._compiled_mo()
        modata = mo.read()
        self.assertIn(
            '\xde\x12\x04',
            modata,
        )
        self.assertIn(
            'Columbo',
            modata,
        )

    def test_filled_message(self):
        # prepare a storage
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.language('de')
        zl.set_version('1', TEST_PO_DE)
        zl.current = '1'

        from collective.zanata.gettextmessagecatalog import LocalGettextMessageCatalog  # noqa
        lm = LocalGettextMessageCatalog(zl)

        self.assertEqual(
            lm.getMessage('Watch Columbo'),
            'Columbo schaun'
        )
        self.assertEqual(
            lm.getMessage('days_and_hours'),
            '$d Tage und $h Stunden'
        )
