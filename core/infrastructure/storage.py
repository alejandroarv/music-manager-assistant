# core/infrastructure/storage.py

import json
import os
import tempfile

class Storage:
    """
    # Low-level persistence layer

    # Responsibilities:
    # - Manage file existence
    # - Read data from disk
    # - Write data to disk

    # IMPORTANT
    # This class doesn't uunderstand:
    # - Bookings
    # - Contracts
    # - Business logic
    # It only knows how to read/write raw data (lists, dicts) to a file
    """
    def __init__(self, file_path):\
        # Path to the JSON storage file (provided by config)
        self.file_path = file_path

        # Ensure the storage file and directory exist
        self._ensure_storage()

    def _ensure_storage(self):
        """
        Ensure storage environment is ready

        Steps:
        1. Create directory if it doesn't exist
        2. Create empty JSON file if it doesn't exist
        """

        # Create directory if missing (e. g., data/)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        # If file does not exist, initialize it with an empty list
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load_all(self):
        """
        Load all records safely.
        """
        try:
            if not os.path.exists(self.file_path):
                return []

            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)

        except json.JSONDecodeError:
            # Corrupted file → recover gracefully
            return []

        except Exception as e:
            raise Exception(f"Failed to load data: {str(e)}")

    def save_all(self, data):
        """
        Safely overwrite storage using atomic write.
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

            # Replace original file atomically
            os.replace(temp_name, self.file_path)

        except Exception as e:
            raise Exception(f"Failed to save data safely: {str(e)}")