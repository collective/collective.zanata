# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.zanata.tests.data import TEST_PO_DE
from collective.zanata.tests.data import TEST_PO_DE_2
from collective.zanata.testing import COLLECTIVE_ZANATA_INTEGRATION_TESTING

import unittest


class TestApi(unittest.TestCase):

    layer = COLLECTIVE_ZANATA_INTEGRATION_TESTING

    def test_create(self):
        from collective.zanata.storage import is_existing_domain
        self.assertFalse(is_existing_domain('testdomain'))

        from collective.zanata import api
        api.create('testdomain')
        self.assertTrue(is_existing_domain('testdomain'))

        from collective.zanata import api
        api.create('otherdomain', languages=['de', 'fr'])
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('otherdomain')
        self.assertListEqual(
            zd.storage.objectIds(),
            ['de', 'fr']

        )

    def test_list_domains(self):
        from collective.zanata import api
        api.create('testdomain')
        api.create('otherdomain')
        self.assertListEqual(
            api.domains(),
            ['otherdomain', 'testdomain'],
        )

    def test_info(self):
        from collective.zanata import api
        api.create('testdomain', languages=['de', 'fr', 'it'])
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zd.settings['foo'] = 'bar'
        zd.language('de').set_version('v1', '#testdata1')
        zd.language('de').set_version('v2', '#testdata2')
        zd.language('de').current = 'v2'
        self.assertDictEqual(
            api.info('testdomain'),
            {
                'languages': {
                    'de': {'v1': {'current': False}, 'v2': {'current': True}},
                    'fr': {},
                    'it': {},
                },
                'permissions': {},
                'settings': {'foo': 'bar'},
            }
        )

    def test_update_language_nonexisting_domain(self):
        from collective.zanata import api
        with self.assertRaises(ValueError):
            api.update_language(
                'testdomain',
                'de',
                'v1',
                current=True,
                data='#testdata1'
            )

    def test_update_language_nonexisting_language(self):
        from collective.zanata import api
        api.create('testdomain')
        with self.assertRaises(ValueError):
            api.update_language(
                'testdomain',
                'de',
                'v1',
                current=True,
                data='#testdata1'
            )

    def test_update_language_initial_non_current(self):
        from collective.zanata import api
        api.create('testdomain', languages=['de'])
        api.update_language(
            'testdomain',
            'de',
            'v1',
            current=True,
            data='#testdata1'
        )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        self.assertIsNotNone(
            queryUtility(ITranslationDomain, name='testdomain')
        )
        from collective.zanata.storage import I18NDomainStorage
        zd = I18NDomainStorage('testdomain')
        zl = zd.language('de')
        self.assertEqual(len(list(zl.storage)), 1)

    def test_update_language_switch_version_one_step(self):
        from collective.zanata import api
        api.create('testdomain', languages=['de'])
        # create initial activated version
        api.update_language(
            'testdomain',
            'de',
            'v1',
            current=True,
            data=TEST_PO_DE
        )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )
        # add a new active version
        api.update_language(
            'testdomain',
            'de',
            'v2',
            current=True,
            data=TEST_PO_DE_2
        )
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo gucken'
        )

    def test_update_language_switch_version_two_step(self):
        from collective.zanata import api
        api.create('testdomain', languages=['de'])
        # create initial activated version
        api.update_language(
            'testdomain',
            'de',
            'v1',
            current=True,
            data=TEST_PO_DE
        )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        ltd = queryUtility(ITranslationDomain, name='testdomain')
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )
        # add a new inactive version
        api.update_language(
            'testdomain',
            'de',
            'v2',
            current=False,
            data=TEST_PO_DE_2
        )
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo schaun'
        )
        # activate version
        api.update_language(
            'testdomain',
            'de',
            'v2',
            current=True,
        )
        self.assertEqual(
            ltd.translate('Watch Columbo', target_language='de'),
            'Columbo gucken'
        )

    def test_update_language_disable_language(self):
        from collective.zanata import api
        LANGS = ['de', 'it', 'fr']
        api.create('testdomain', languages=LANGS)
        for lang in LANGS:
            api.update_language(
                'testdomain',
                lang,
                'v1',
                current=True,
                data='#testdata1 {0}'.format(lang)
            )
        from zope.component import queryUtility
        from zope.i18n import ITranslationDomain
        self.assertIsNotNone(
            queryUtility(ITranslationDomain, name='testdomain')
        )
