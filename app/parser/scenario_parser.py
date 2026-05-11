import re

from app.utils.logger import setup_logger

logger = setup_logger(__name__)

SCENARIO_PATTERN = r"^[A-Z]{3}-\d{3}$"


def extract_scenarios(rows, sheet_name):

    scenarios = []

    current_scenario = None

    for row in rows:

        values = row["values"]

        if not values:
            continue

        scenario_id = values[0]
        parameter_name = values[1]
        parameter_value = values[2]
        scenario_title = values[3]

        # Skip empty rows
        if not scenario_id and not parameter_name:
            continue

        # VALID scenario detection
        if scenario_id and re.match(
            SCENARIO_PATTERN,
            str(scenario_id)
        ):

            logger.info(
                f"New Scenario Detected: {scenario_id}"
            )

            if current_scenario:
                scenarios.append(current_scenario)

            current_scenario = {
                "sheet_name": sheet_name,
                "scenario_id": str(scenario_id),
                "scenario_title_jp": str(scenario_title)
                if scenario_title else "",
                "parameters": {}
            }

        # Add parameters
        if current_scenario and parameter_name:

            current_scenario["parameters"][
                str(parameter_name)
            ] = str(parameter_value)

    # Add last scenario
    if current_scenario:
        scenarios.append(current_scenario)

    logger.info(
        f"Total Scenarios Extracted: {len(scenarios)}"
    )

    return scenarios