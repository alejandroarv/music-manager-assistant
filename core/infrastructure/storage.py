# core/infrastructure/storage.py

import json
import os
import tempfile

class Storage:
    """
    Low-level JSON persistence layer

    Responsibilities:
    - Ensure storage files/directories exist
    - Read raw data from disk
    - Persist raw data to disk safely

    This class is intentionally generic and contains no business-specific
    logic related to bookings, contracts, tours, or domain entities
    """

    def __init__(self, file_path):
        """
        Initialize the sotrage layer

        Args:
            file_path: Path to the JSON storage file
        """

        self.file_path = file_path

        # Ensure the storage environment exists before use
        self._ensure_storage()

    def _ensure_storage(self):
        """
        Prepare the storage environment

        Creates:
        - The parent directory if missing
        - An empty JSON file if one does not exist
        """

        # Create directory if needed
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # Initialize storage file with an empty list
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_all(self):
        """
        Load all and return all sotred records

        Returns:
            lists: Parsed JSON data from storage

        If the file is corrupted or invalid JSON, an empty
        list is returned as a safe fallback
        """
        try:
            if not os.path.exists(self.file_path):
                return []

            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError:
            # Recover gracefully from corrupted JSON files
            return []

        except Exception as e:
            raise Exception(f"Failed to load data: {str(e)}")

    def save_all(self, data):
        """
        Persist all records using an atomic write operation

        Data is first written to a temporary file and then atomically replaces
        the original file to reduce the risk of corruption during writes
        """
        try:
            dir_name = os.path.dirname(self.file_path)

            # Write to temp file first
            with tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,
                dir=dir_name,
                encoding="utf-8"
            ) as tmp_file:
                json.dump(data, tmp_file, indent=4)
                temp_name = tmp_file.name

            # Atomically replace the original file
            os.replace(temp_name, self.file_path)

        except Exception as e:
            raise Exception(f"Failed to save data safely: {str(e)}")