import os

folders = [
    "app",
    "app/parser",
    "app/models",
    "app/config",
    "app/utils",
    "input",
    "output",
    "logs"
]

files = [
    "app/__init__.py",

    "app/parser/__init__.py",
    "app/parser/excel_reader.py",
    "app/parser/sheet_parser.py",
    "app/parser/scenario_parser.py",
    "app/parser/parameter_mapper.py",
    "app/parser/json_builder.py",

    "app/models/__init__.py",
    "app/models/schemas.py",

    "app/config/parser_config.yaml",

    "app/utils/__init__.py",
    "app/utils/helpers.py",
    "app/utils/logger.py",

    "main.py",
    "requirements.txt",
    "README.md"
]

print("\nCreating folders...\n")

for folder in folders:

    os.makedirs(folder, exist_ok=True)

    print(f"[CREATED] Folder -> {folder}")

print("\nCreating files...\n")

for file in files:

    if not os.path.exists(file):

        with open(file, "w", encoding="utf-8") as f:
            pass

        print(f"[CREATED] File -> {file}")

    else:

        print(f"[EXISTS] File -> {file}")

print("\nProject structure created successfully.")