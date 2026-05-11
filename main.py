import json

from app.parser.excel_reader import load_excel
from app.parser.sheet_parser import parse_sheet
from app.parser.scenario_parser import extract_scenarios
from app.parser.json_builder import save_json
from app.parser.parameter_mapper import normalize_parameters


INPUT_FILE = "input/ADAS_Scenarios_JP.xlsx"


def main():

    workbook = load_excel(INPUT_FILE)

    all_scenarios = []

    for sheet_name in workbook.sheetnames:

        # Skip overview sheet
        if "Overview" in sheet_name or "概要" in sheet_name:
            continue

        sheet = workbook[sheet_name]

        rows = parse_sheet(sheet)

        scenarios = extract_scenarios(
            rows,
            sheet_name
        )

        for scenario in scenarios:
            scenario["parameters_canonical"] = normalize_parameters(
            scenario["parameters"]
                                    )

        all_scenarios.extend(scenarios)

    # Save JSON file
    save_json(all_scenarios)

    # Print JSON in terminal only
    print(
        json.dumps(
            all_scenarios[1],
            indent=4,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":

    main()