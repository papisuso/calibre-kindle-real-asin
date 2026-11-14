# Kindle Real ASIN (calibre plugin)

Sideload books to a newer Kindle with calibre, have them show up as **Books** (not Documents), **with their cover**.

## The problem

- Books sent with Amazon's *Send to Kindle* always become personal documents ("Docs").
- Books converted to AZW3 with calibre and sent over USB show up as Books, but on newer Kindles they often have **no cover**.

Why: for a Book (cdetype `EBOK`) the Kindle does not take the cover from the file. It uses a thumbnail in `system/thumbnails`, or it downloads the cover from Amazon using the book's ASIN. calibre does try to place that thumbnail when sending over USB, but on newer Kindles that connect over MTP the cover can still be missing (on the device this was tested on, the `system` folder is not even visible over USB). And calibre writes the book's own calibre UUID as the ASIN (EXTH record 113), even when the book has a real Amazon identifier. So the Kindle cannot fetch the cover from Amazon either.

## What the plugin does

It replaces calibre's built-in MOBI metadata writer for AZW3, MOBI and AZW files. It writes the same metadata calibre writes and, if the book has an Amazon identifier that looks like a Kindle ASIN (`B` + 9 characters), it writes that ASIN into EXTH 113 and 504 and sets cdetype `EBOK`.

With Wi-Fi on, the Kindle then downloads the cover from Amazon. The book stays a Book.

It runs wherever calibre writes metadata into a file: when you **send a book to the device**, and when you use **Embed metadata** in the library.

## Requirements

- calibre 7.0 or newer (tested with 9.18 on macOS)
- The book must exist as a Kindle edition in the Amazon store your Kindle is registered to
- Wi-Fi on the Kindle, so it can fetch the cover

## Install

1. Download `kindle_real_asin.zip` from the Releases page (or build it with `./build.sh`).
2. In calibre: **Preferences > Plugins > Load plugin from file**, choose the zip.
3. Restart calibre.

## Use

1. Make sure the book has an Amazon identifier in **Edit metadata > Ids**, for example `amazon:B0XXXXXXXX` (or `amazon_de:`, `amazon_es:`, ... or `mobi-asin:`). *Download metadata* often adds it. Otherwise copy the ASIN from the Kindle edition's page on Amazon.
2. Convert to AZW3 if needed.
3. Connect the Kindle by USB and use **Send to device**.
4. Keep Wi-Fi on. The cover appears after a short while.

## Settings (optional)

In **Preferences > Plugins**, select *Kindle Real ASIN* and click **Customize plugin**. Enter your Amazon store(s) in order of preference, for example `es, de`, `co.uk` or `com`. Identifiers from these stores are used first, before any other identifier.

Order without settings: `mobi-asin`, then `amazon` (amazon.com), then any other `amazon_xx`. Only values that look like a Kindle ASIN count, so calibre's own UUIDs in `mobi-asin` and ISBNs are skipped.

## Notes and limits

- Tested on one device so far: Kindle Paperwhite Signature Edition (MTP). Reports from other models are welcome.
- Books without a Kindle edition on Amazon still get no cover. There is no ASIN to point to.
- Books you have marked as personal documents with calibre's MOBI output option *Personal Doc tag* stay personal documents.
- KFX files are not handled.
- *Embed metadata* also writes the real ASIN into the files in your library. That is intended.
- Books already on the Kindle are not changed. Send them again after installing the plugin.

## Uninstall

**Preferences > Plugins**, select *Kindle Real ASIN*, **Remove plugin**, restart calibre. calibre's built-in writer takes over again.

## License

GPL v3, see [LICENSE](LICENSE).

Not affiliated with Amazon. Kindle is a trademark of Amazon.com, Inc.
