# Cell reference data and their limits

[← Back to overview](../README.md)

**Lighthouse does not determine the physical location of a device.** It reconstructs which network cell served a device when a record was created, and shows that cell on a map. The device can have been anywhere in the cell's coverage area, and that area is not known from the CDR. A movement path drawn between cells is a hypothesis about the serving cells, not a measured route.

## Where each piece of location information comes from

| Information | Source | Evidentiary status |
|---|---|---|
| Cell ID, MCC/MNC, LAC/TAC | CDR (decoded ULI) | Evidence-derived |
| Cell coordinates and azimuth | CDR (operator-reported, where present) | Evidence-derived (operator data) |
| Tower coordinates | OpenCelliD (lookup levels 1–3), nearest known cell (level 4), beaconDB (level 5, optional) | External, crowdsourced estimate; lookup level shown |
| Range | OpenCelliD | Uncertainty of the estimated position, **not** coverage |
| Sector wedge | Drawn from the azimuth | Schematic (fixed opening angle of 44°) |
| Distance between consecutive cells | Computed (great circle) | Derived; not the distance travelled by the device |
| Device position | – | Not available; only "somewhere within the serving cell's coverage area" |

Lighthouse does not estimate the distance between a device and its cell: exports of this kind usually contain neither timing advance nor signal measurements.

## The 44° wedge

Cells with an operator-reported azimuth are drawn as a wedge with an opening angle of 44°. This marks the main direction of the antenna. It is **not** a coverage estimate: it is deliberately narrower than the half-power beamwidth of a typical macro-cell sector antenna (70° in the 3GPP evaluation model, TR 36.814) and than the 120° served by each sector of a three-sector site, so that it is not mistaken for the served area, but wide enough not to suggest a precision of a few degrees.

## OpenCelliD lookup levels

For cells without operator coordinates, Lighthouse looks up the decoded cell identity in a locally stored copy of [OpenCelliD](https://opencellid.org). Each result is labelled with the level that produced it:

1. **Exact match** on operator (MNC), location/tracking area and cell identity.
2. **Base-station centroid** (LTE/NR): sample-weighted centroid of all known sectors of the same base station, when the sector itself is missing.
3. **Same centroid** when the decoded area code is itself a base-station identifier.
4. **Nearest known cell** within 10 km of coordinates contained in the record, preferring the same operator.
5. **beaconDB** (optional, online): query to the open [beaconDB](https://beacondb.net) service, sending only the cell identity.

Levels 2–5 give progressively weaker statements. A centroid is not the position of the serving sector. A level-4 result is a **different** cell near the reported position; it only makes the record visible on the map and must not be reported as the serving cell.

## Why crowdsourced positions are estimates

OpenCelliD positions are estimated from measurements that volunteers' phones report together with their own GPS position; operators do not supply them. An estimate therefore tends to lie where measurements were taken, typically along roads and in built-up areas, rather than at the antenna. Cells with few measurements can be far off. Coverage is uneven: in our test region several LTE base stations of one operator are missing entirely. The `range` field is often read as a coverage radius, but it describes the uncertainty of the estimated position. Neither OpenCelliD nor beaconDB provides azimuth, beamwidth or transmit power.

## For reports and court

- Crowdsourced cell positions support orientation and hypotheses, **not an opinion on where a device was**.
- The authoritative source for cell positions and antenna parameters is the **operator's cell database**, obtained through the same legal channel as the CDRs.
- Statements about coverage require **radio-frequency surveys** of the relevant cells.
- Lighthouse keeps operator-reported positions and external estimates in separate layers and never writes an external estimate into the case database.
