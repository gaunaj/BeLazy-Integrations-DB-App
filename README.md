# BeLazy JSON Field Editor

A simple, cross-platform desktop app to edit JSON files with a user-friendly interface.

## Features
- Change the value of any field in a JSON array of objects.
- Rename fields (columns) safely, with validation to prevent accidental overwrites.
- See all available fields in dropdown menus for easy selection.
- Get instant feedback and color-coded logs for success and errors.
- **Automatically create a backup of your JSON file before any changes.**
- Modern, blue-themed interface with the BeLazy logo.

## How Backups Work
- Every time you make a change (either changing a value or renaming a field), the app creates a backup of your JSON file before saving any modifications.
- The backup file is created in the same folder and has the same name as your original file, but with `.backup` added at the end (e.g., `data.json.backup`).
- If you need to revert to the previous state, simply rename or restore the `.backup` file.
- Each new change will overwrite the previous backup.

## Requirements
- Python 3.8+
- Not supported by python 3.13
- Install dependencies:

```
pip install -r requirements.txt
```

## How to Use

1. **Clone or download this repository.**
2. **Place your JSON file** (array of objects) in the project folder, or have its path ready.
3. **Run the app:**

```
python json_field_editor_app.py
```

4. **Select your JSON file** using the 'Browse' button or by entering the path.
5. **To change a field value:**
    - Select the field (column) from the dropdown.
    - Enter the value to search for and the new value.
    - Click 'Change Value'.
6. **To rename a field:**
    - Select the old field name from the dropdown.
    - Enter the new field name (must not already exist).
    - Click 'Change Name'.
7. **Check the log area** for color-coded feedback and error messages.
8. **A backup** of your JSON file will be created automatically before any changes.

## Notes
- The app only works with JSON files that are arrays of objects (like a table).
- The logo must be named `BeLazy logo.jpg` and placed in the same folder as the app for it to display.
- No native dependencies required—just Python and the packages in `requirements.txt`.

## License
MIT
