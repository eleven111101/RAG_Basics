from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def parse_sheet(sheet):

    logger.info(f"Parsing Sheet: {sheet.title}")

    rows = []

    for idx, row in enumerate(sheet.iter_rows(values_only=True), start=1):

        rows.append({
            "row_number": idx,
            "values": list(row)
        })

    logger.info(
        f"Total Rows Parsed: {len(rows)}"
    )

    return rows