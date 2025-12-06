from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    completed: bool = False
    priority: str = "medium"
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": int(self.completed),
            "priority": self.priority,
            "tags": ",".join(self.tags) if self.tags else None,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_row(row):
        if row is None:
            return None
        # support sqlite3.Row access by name
        try:
            id_ = row["id"]
            title = row["title"]
            description = row["description"]
            due_date = row["due_date"]
            completed = bool(row["completed"])
            priority = row["priority"] if "priority" in row.keys() else "medium"
            tags_raw = row["tags"] if "tags" in row.keys() else None
            created_at = row["created_at"]
        except Exception:
            # fallback to index-based
            id_ = row[0]
            title = row[1]
            description = row[2]
            due_date = row[3]
            completed = bool(row[4])
            priority = row[6] if len(row) > 6 else "medium"
            tags_raw = row[7] if len(row) > 7 else None
            created_at = row[5]

        tags = [] if not tags_raw else [t for t in (tags_raw.split(",") if isinstance(tags_raw, str) else []) if t]
        return Task(
            id=id_,
            title=title,
            description=description,
            due_date=due_date,
            completed=completed,
            priority=priority,
            tags=tags,
            created_at=created_at,
        )
