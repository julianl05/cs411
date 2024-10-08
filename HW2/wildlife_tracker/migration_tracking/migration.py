from typing import Any

from wildlife_tracker.migration_tracking.migration_path import MigrationPath

class Migration:
    def __init__(self,
                 start_date: str,
                 current_date: str,
                 current_location: str,
                 migration_id: int,
                 migration_path: MigrationPath,
                 status: str = "Scheduled") -> None:
        self.start_date = start_date
        self.current_date = current_date
        self.current_location = current_location
        self.migration_id = migration_id
        self.migration_path = migration_path
        self.status = status
        pass

    def get_migration_details(self) -> dict[str, Any]:
        pass

    def update_migration_details(self, **kwargs: Any) -> None:
        pass