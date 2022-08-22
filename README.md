# CsvToIconDb

Create a WoW icon database from a CSV file.

## Instructions

1. Navigate to [WoW.tools Database Browser](https://wow.tools/dbc/?dbc=manifestinterfacedata&build=3.4.0.45189).
2. Select the desired build.
3. Download the CSV file.
4. Run `update-icon-db.py` (required arguments below).

## update-icon-db.py

The available command-line arguments are:

Argument         | Required | Description
--------         | -------- | -----------
`--input`        | Yes      | The input .csv file, acquired from above
`--output`       | Yes      | The output .lua file
`--blacklist`    | No       | An optional file containing `fd_id`s that should be ignored, one per line
`--namespace`    | Yes      | The namespace that the Lua file will be placed in
`--create-addon` | No       | An optional parameter that enables creation of an AceAddon
`--function`     | Yes      | The function that will expose the icons for external code

### Example (Retail)

```python
py .\update-icon-db.py --input ".\manifestinterfacedata.csv" --output "MediaRetail.lua" --blacklist ".\icon-blacklist-retail.txt" --namespace "IconDB" --function "GetIcons"
```
