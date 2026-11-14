# Kindle Real ASIN, a calibre plugin
# License: GPL v3 (see LICENSE)
"""
Writes the real Kindle store ASIN into AZW3, MOBI and AZW files.

When calibre converts or embeds metadata into a MOBI/AZW3 file it stores the
book's calibre UUID as the ASIN (EXTH record 113). Kindles show the cover of a
book (cdetype EBOK) either from a thumbnail in system/thumbnails or by fetching
it from Amazon using the ASIN. calibre does try to place such a thumbnail when
sending over USB, but on newer Kindles that connect over MTP sideloaded books
can still end up without a cover.

This plugin replaces calibre's built-in MOBI metadata writer. It writes exactly
the same metadata as calibre and, if the book has an Amazon identifier that
looks like a Kindle ASIN, writes that ASIN into the file (EXTH 113 and 504,
cdetype EBOK). The Kindle then downloads the cover from Amazon (Wi-Fi needed)
and the book stays a book instead of a personal document.

It runs wherever calibre writes metadata into a file, most importantly when
sending books to the device.
"""

import re

from calibre.customize import MetadataWriterPlugin

# Kindle ASINs start with "B" and have 10 characters. This rules out ISBN-10
# values of print editions and calibre's own UUIDs.
ASIN_RE = re.compile(r'^B[0-9A-Z]{9}$')


def parse_stores(customization):
    """'es, de' -> ['amazon_es', 'amazon_de']; 'com' or 'us' -> ['amazon']."""
    keys = []
    for part in re.split(r'[\s,;]+', (customization or '').strip().lower()):
        part = part.strip().strip('.').strip('/')
        if not part:
            continue
        for prefix in ('https://', 'http://', 'www.', 'amazon.'):
            if part.startswith(prefix):
                part = part[len(prefix):]
        # calibre uses amazon_uk, amazon_jp, amazon_au, amazon_br ...
        part = re.sub(r'^(co|com)\.', '', part)
        if part in ('com', 'us', 'amazon'):
            key = 'amazon'
        else:
            key = 'amazon_' + part.replace('.', '_')
        if key not in keys:
            keys.append(key)
    return keys


def find_asin(mi, preferred_stores=()):
    try:
        ids = mi.get_identifiers() or {}
    except Exception:
        ids = getattr(mi, 'identifiers', None) or {}
    ids = {str(k).lower(): str(v).strip().upper() for k, v in ids.items() if v}
    # The stores chosen by the user win, then mobi-asin, then amazon.com,
    # then any other Amazon store.
    keys = [*preferred_stores]
    for key in ('mobi-asin', 'amazon'):
        if key not in keys:
            keys.append(key)
    keys += sorted(k for k in ids if k.startswith('amazon_') and k not in keys)
    for key in keys:
        val = ids.get(key)
        if val and ASIN_RE.match(val):
            return val
    return None


def is_personal_doc(mi):
    """True if calibre itself would mark the file as a personal document (MOBI output option 'Personal Doc tag')."""
    try:
        from calibre.ebooks.conversion.config import load_defaults

        tag = load_defaults('mobi_output').get('personal_doc', None)
    except Exception:
        return False
    tags = mi.tags or ()
    # calibre only applies the tag when the book has tags at all.
    return bool(tag) and bool(tags) and (tag == '*' or tag in tags)


class KindleRealASIN(MetadataWriterPlugin):
    name = 'Kindle Real ASIN'
    description = (
        'Writes the real Kindle ASIN from the book identifiers (amazon, amazon_xx, mobi-asin) '
        'into AZW3, MOBI and AZW files when sending to the device or embedding metadata, '
        'so the Kindle shows the cover and the book stays a book.'
    )
    supported_platforms = ['windows', 'osx', 'linux']
    author = 'papisuso'
    version = (1, 1, 0)
    file_types = {'azw3', 'mobi', 'azw'}
    minimum_calibre_version = (7, 0, 0)

    def customization_help(self, gui=False):
        return (
            'Optional: your Amazon store(s) in order of preference, separated by commas, '
            'for example "es, de" or "co.uk". Identifiers from these stores are used first. '
            'Leave empty to use mobi-asin, then amazon.com, then any other store.'
        )

    def set_metadata(self, stream, mi, type):
        from calibre.ebooks.metadata.mobi import MetadataUpdater

        stores = parse_stores(getattr(self, 'site_customization', '') or '')
        asin = find_asin(mi, stores)
        if asin is not None and is_personal_doc(mi):
            # Deliberately marked as a personal document: do not turn it into a book.
            asin = None
        mu = MetadataUpdater(stream)
        if asin is not None:
            # Stop calibre from also adding a random UUID as record 113.
            mu.original_exth_records.setdefault(113, b'')
        mu.update(mi, asin=asin)
