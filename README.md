# Kindle Real ASIN (calibre plugin)

Sideload books to a newer Kindle with calibre, have them show up as **Books** (not Documents), **with their cover**.

## The problem

- Books sent with Amazon's *Send to Kindle* always become personal documents ("Docs").
- Books converted to AZW3 with calibre and sent over USB show up as Books, but on newer Kindles they often have **no cover**.

Why: for a Book (cdetype `EBOK`) the Kindle does not take the cover from the file. It uses a thumbnail in `system/thumbnails`, or it downloads the cover from Amazon using the book's ASIN. calibre does try to place that thumbnail when sending over USB, but on newer Kindles that connect over MTP the cover can still be missing (on the device this was tested on, the `system` folder is not even visible over USB). And calibre writes the book's own calibre UUID as the ASIN (EXTH record 113), even when the book has a real Amazon identifier. So the Kindle cannot fetch the cover from Amazon either.

## Before you use this: the KFX Output plugin already does this

The established [KFX Output plugin](https://www.mobileread.com/forums/showthread.php?t=272407) by jhowell gives the same result, and for most people it is the better choice:

1. Install Kindle Previewer (KFX Output needs it for the conversion) and the KFX Output plugin.
2. Make sure the book has the real ASIN in its Amazon identifier (see *Use* below).
3. Convert to KFX with the option **Create book (EBOK)** checked (Convert books > KFX Output). Without that option the result is a personal document, even if the ASIN is present.
4. Send the KFX to the device.

Checked with KFX Output 2.22.0 and Kindle Previewer 4.0.4: the KFX file gets the real ASIN and cdetype `EBOK`, the same values this plugin writes into AZW3. KFX also gives you Amazon's enhanced typesetting.

This plugin only makes sense if you want to stay with AZW3, for example to avoid installing Kindle Previewer or because a book fails to convert to KFX.

Thanks to the r/Calibre commenters who pointed this out.

## Risk: sideloaded "Books" can be removed

Users report that sideloaded books marked as `EBOK` (AZW3 or KFX, with this plugin or with KFX Output) can be deleted by the Kindle when it reconnects after being offline or in airplane mode for a long time. This is not confirmed by Amazon, but it applies to every route that makes a sideloaded book a Book. Keep your books in calibre so you can send them again, and keep Wi-Fi on. Personal documents (`PDOC`) are not affected.

If you mainly want covers and are fine with Docs, a personal document is the safer option. If you also want the book in the cloud and reading position sync between devices, use Send to Kindle (it always files books under Docs).

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
