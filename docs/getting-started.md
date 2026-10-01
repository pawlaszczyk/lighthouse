# Getting started

[← Back to overview](../README.md)

## 1. Install FQLite

Download the installer for your platform from the [latest FQLite release](https://github.com/pawlaszczyk/fqlite/releases/latest) (macOS `.dmg`, Windows `.exe`, Linux `.deb`) and install it as usual. Lighthouse is included from FQLite 5.0 onwards; no separate installation is needed.

### Build from source

Until a release with Lighthouse is available, or to use the newest development state:

```bash
git clone https://github.com/pawlaszczyk/fqlite.git
cd fqlite
./gradlew run          # requires JDK 21
```

On macOS, `./run-fqlite.sh` looks for a JDK 21 (for example `brew install openjdk@21`) and starts FQLite with it.

## 2. Import an ETSI export

1. Start FQLite and choose **File → Open Database…**, or drag the XML file onto the start window.
2. Select one or more ETSI TS 102 657 `RetainedData` XML files. Several files are merged into one SQLite database, created next to the first file (`<name>.sqlite`). Every row keeps the name of its source file in the column `source_file`.
3. The database opens like any other SQLite file in FQLite. Besides `response_records`, it contains `request_metadata` and `import_log` (SHA-256 of every source file before and after the import, record counts, importer version, data-quality warnings).

No real data at hand? Use the two synthetic exports in [`data/synthetic-case`](../data/synthetic-case).

> [!NOTE]
> All timestamps are stored and shown in **UTC**. German local time is one hour (winter) or two hours (summer) ahead. Convert clock times accordingly when you filter or ask the assistant.

## 3. Open Lighthouse

Select the table `response_records` in the tree on the left and click the **Lighthouse** button (lighthouse icon) in the toolbar. The button is enabled only for this table.

The window has three tabs: **Map & Timeline**, **MOC/MTC** (a map of calls only, coloured by outgoing/incoming) and **Statistics** (the 23 analysis presets). The question field for the assistant is at the bottom of the window.

## 4. Optional settings

Open **Settings → Location**:

| Setting | Purpose | Source |
|---|---|---|
| Local map (`.mbtiles`) | Map tiles without internet access | For example an OpenStreetMap extract for your country in MBTiles format |
| OpenCelliD export | Estimated cell positions for cells without operator coordinates | [opencellid.org/downloads.php](https://opencellid.org/downloads.php) (free registration; country file, e.g. `262.csv` for Germany) |
| beaconDB | Online fallback for cells missing from OpenCelliD (sends only the cell identity) | No key needed; off unless enabled |
| TAC database / device lookup | Handset make and model from the IMEI | Local TAC list; optional online lookup with API key (sends 8 digits of the IMEI) |

Please read [Cell reference data and their limits](cell-reference-data.md) before you use OpenCelliD positions in a report.

## 5. Set up the query assistant

The assistant needs a language model file (`.gguf`) on your computer. When you use it for the first time without a model, FQLite opens the LLM configuration dialog:

- **Browse…** selects a model file you have already downloaded, or
- **Download LLM** fetches a model from Hugging Face.

For ETSI data, use the Lighthouse model: [`pawlaszc/Lighthouse-ETSI-CDR-Text2SQL`](https://huggingface.co/pawlaszc/Lighthouse-ETSI-CDR-Text2SQL). Two sizes are available:

| File | Size | When to use |
|---|---|---|
| Q8_0 | 3.4 GB | Default; best accuracy |
| Q4_K_M | 2.0 GB | Computers with little memory |

The model runs on ordinary hardware. FQLite uses a compatible GPU if one is available (Apple Silicon via Metal) and otherwise falls back to the CPU; the status bar shows the active mode.

Then type a question into the field at the bottom of the Lighthouse window and click **Ask**. See [Query assistant](query-assistant.md) for what it can and cannot do.
