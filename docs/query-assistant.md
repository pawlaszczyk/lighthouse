# Query assistant

[← Back to overview](../README.md)

The assistant lets you ask questions about the imported records in German or English instead of writing SQL. It translates the question into an SQL query and runs it against the case database. The answer therefore consists of records from your own data, not of text generated from the model's general knowledge (*database-grounded* querying).

## Examples

- *Welche IMSI gehört zur Rufnummer 4917…?* / *Which IMSI belongs to number 4917…?*
- *Show all roamers on 15 September 2026 between 1:00 and 11:00.*
- *Wie viele SMS hat 4915… gesendet?*
- *Which numbers were in cell 30002/3 on 20 May?*
- *Wann war der letzte Datensatz des Geräts mit der IMEI 35…?*

## How a question is processed

1. **Routing.** The model first classifies the question. If it matches one of the [analysis presets](presets.md) (co-location, calls or SMS by direction, numbers from a country, subscribers in several cells, device/SIM changes, plain time filters), the reviewed preset query answers it. Deterministic keyword rules correct recurring misclassifications.
2. **SQL generation.** All other questions go to the SQL generator. It receives the annotated database schema and an automatically generated description of the loaded case (which files, identifiers and cells it contains).
3. **Checks and repair.** Deterministic rules fix known error patterns: time-of-day comparisons, an identifier searched in the wrong column (for example a phone number in the IMSI column), and unknown aggregate aliases.
4. **One retry.** If SQLite still rejects the query, the model gets the error message and generates the query once more.
5. **Result.** Results with a position appear on the map. Counts, lists of contacts and other results open in a result window together with the question and the executed SQL.

## The model

| | |
|---|---|
| Base model | Llama 3.2 3B Instruct |
| Training | Two stages with LoRA: (1) general forensic SQLite text-to-SQL ([`pawlaszc/DigitalForensicsText2SQLite`](https://huggingface.co/pawlaszc/DigitalForensicsText2SQLite)), (2) adaptation to the Lighthouse ETSI schema with the data in [`data/training`](../data/training), plus replay of stage-1 examples against forgetting |
| Format | GGUF, Q8_0 (3.4 GB, default) or Q4_K_M (2.0 GB) |
| Runtime | [llama.cpp](https://github.com/ggml-org/llama.cpp) via java-llama.cpp, inside FQLite; GPU if available, otherwise CPU |
| Download | [`pawlaszc/Lighthouse-ETSI-CDR-Text2SQL`](https://huggingface.co/pawlaszc/Lighthouse-ETSI-CDR-Text2SQL) |

The model runs entirely on the examiner's computer. No question and no case data are sent to an external AI service.

## Limits: please read

- **An executable query is not necessarily a correct one.** Most remaining errors in our evaluation were plausible-looking: the query runs and returns records, but answers a slightly different question (for example a wrong time boundary, a missing direction filter, or MIN instead of MAX). Check every answer against the displayed SQL and the underlying records before you rely on it.
- **Use the presets for recurring questions.** Their queries are reviewed and deterministic; the assistant's are not.
- **Times are UTC.** A clock time in a question is compared with UTC timestamps. German local time is one or two hours ahead.
- **The model knows this schema only.** It was trained for databases created by the Lighthouse ETSI import. For other SQLite databases, use FQLite's general SQL agent with the stage-1 model.
- **Evaluation data are synthetic.** The model was trained and tested on synthetic, ETSI-conformant data. Real exports can contain field variants that did not occur there.

Detailed results, including comparisons with untrained local models and a cloud-hosted model and an error analysis, are in the accompanying article. The test sets are in [`data/test-sets`](../data/test-sets).
