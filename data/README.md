# Data

[← Back to overview](../README.md)

Everything in this folder is **synthetic**. No real call detail records, subscribers or case data are included. Licence: [CC BY 4.0](LICENSE). Checksums: [`SHA256SUMS`](SHA256SUMS).

## `synthetic-case/`: test case

Two ETSI TS 102 657-conformant `RetainedData` exports, linked by a fictitious investigation, and the database created from them by the Lighthouse import.

| File | Content |
|---|---|
| `ETSI-Testdaten-45.xml` | Border region Saxony/Czech Republic: 45 subscribers, 5 cells, 172 records, 20 May 2026 (request number `…TEST45`) |
| `ETSI-Testdaten-Dresden.xml` | Urban setting in Dresden: 3 cells, 190 records, 22 May 2026 (request number `…TESTDD`) |
| `case_merged.db` | Both files imported into one SQLite database: 506 rows in `response_records` (one row per party leg or data session), `request_metadata` |

Two subscribers appear in both exports. Open the XML files in FQLite to try Lighthouse (see [Getting started](../docs/getting-started.md)). All reference answers of the test sets below were obtained by executing the reference SQL against `case_merged.db`.

Cell identities are realistic in form; subscriber numbers, IMSIs and IMEIs are invented.

## `training/`: training data of the query model (stage 2)

One JSON array per file. Each entry has `instruction` (question), `context` (schema and case description), `response` (reference SQL), plus `difficulty`, `lang` and further metadata. Most questions exist in German and English with the same reference SQL.

| File | Entries | Content |
|---|---|---|
| `lighthouse_etsi_cdr_training_dataset.json` | 138 | Core set (36 easy, 36 medium, 66 hard); 10 % of its questions form the validation split used for checkpoint selection |
| `lighthouse_etsi_cdr_targeted_train.json` | 230 | Targeted examples for error patterns found in earlier rounds (+ `_report.json`) |
| `lighthouse_etsi_cdr_paraphrase_train_clean.json` | 320 | Paraphrases; 64 references cleaned of a source-file filter the question did not ask for (+ `_report.json`) |
| `lighthouse_etsi_cdr_basic_train.json` | 744 | Generated basic questions in 28 families: identifiers, IMSI/IMEI/APN mappings, first/last record, calls and SMS by direction, cells in several notations, time windows (+ `_report.json`) |

## `test-sets/`: frozen test sets

Each test set has a manifest with its SHA-256, creation date and the rules under which it was created. Test sets were never used for training. The training script refuses files marked as hold-out and removes training examples whose reference SQL occurs in the validation split; `basic_train` was additionally checked against all four test sets (question similarity < 0.80, no identical reference SQL).

| File | Name in the article | Entries | Difficulty | Notes |
|---|---|---|---|---|
| `lighthouse_etsi_cdr_HOLDOUT_V3.json` | Hold-out A | 112 | medium, hard | |
| `lighthouse_etsi_cdr_HOLDOUT_V4.json` | Hold-out B | 120 | medium, hard | 20 references restrict to a source file that the question does not mention; results are also reported for the 100 well-posed entries |
| `lighthouse_etsi_cdr_HOLDOUT_C.json` | Hold-out C | 96 | easy | Used for the error analysis; its error types informed `basic_train`, so it is no longer an independent test of later models |
| `lighthouse_etsi_cdr_HOLDOUT_D.json` | Hold-out D | 144 | 114 easy, 30 medium | Frozen before `basic_train` was generated. Uses the same question families as `basic_train` with different wording, parameters and reference SQL, so it measures mastery of these basic concepts rather than robustness to free wording |

## Scoring

A generated query counts as correct if its result set equals that of the reference query (strict, including order where the reference sorts). Order-insensitive accuracy and the share of executable queries are reported in addition.
