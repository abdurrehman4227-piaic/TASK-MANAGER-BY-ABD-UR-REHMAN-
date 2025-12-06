import sqlite3
from typing import List, Optional
from .models import Task

class SQLiteStorage:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._ensure_table()

    def _ensure_table(self):
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                completed INTEGER DEFAULT 0,
                priority TEXT DEFAULT 'medium',
                tags TEXT,
                created_at TEXT
            )
            """
        )
        self._conn.commit()
        # Ensure backward compatibility: add missing columns if table existed without them
        cur.execute("PRAGMA table_info(tasks)")
        cols = {r[1] for r in cur.fetchall()}  # name is at index 1
        if "priority" not in cols:
            cur.execute("ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'medium'")
        if "tags" not in cols:
            cur.execute("ALTER TABLE tasks ADD COLUMN tags TEXT")
        self._conn.commit()

    def add_task(self, title: str, description: Optional[str]=None, due_date: Optional[str]=None, priority: str = "medium", tags: Optional[str] = None) -> Task:
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        cur = self._conn.cursor()
        created_at = Task(id=None, title=title, description=description, due_date=due_date).created_at
        cur.execute(
            "INSERT INTO tasks (title, description, due_date, completed, priority, tags, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (title, description, due_date, 0, priority, tags, created_at),
        )
        self._conn.commit()
        task_id = cur.lastrowid
        tags_list = [] if not tags else [t for t in tags.split(",") if t]
        return Task(id=task_id, title=title, description=description, due_date=due_date, completed=False, priority=priority, tags=tags_list, created_at=created_at)

    def delete_task(self, task_id: int) -> bool:
        cur = self._conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self._conn.commit()
        return cur.rowcount > 0

    def update_task(self, task_id: int, title: Optional[str]=None, description: Optional[str]=None, due_date: Optional[str]=None, priority: Optional[str]=None, tags: Optional[str]=None) -> Optional[Task]:
        existing = self.get_task(task_id)
        if not existing:
            return None
        new_title = title if title is not None else existing.title
        new_description = description if description is not None else existing.description
        new_due = due_date if due_date is not None else existing.due_date
        new_priority = priority if priority is not None else existing.priority
        new_tags = tags if tags is not None else (",".join(existing.tags) if existing.tags else None)
        cur = self._conn.cursor()
        cur.execute(
            "UPDATE tasks SET title = ?, description = ?, due_date = ?, priority = ?, tags = ? WHERE id = ?",
            (new_title, new_description, new_due, new_priority, new_tags, task_id),
        )
        self._conn.commit()
        return self.get_task(task_id)

    def list_tasks(self, include_completed: bool = True, search: Optional[str]=None, priority: Optional[str]=None, tag: Optional[str]=None, due_before: Optional[str]=None, due_after: Optional[str]=None, sort_by: str = "due_date", order: str = "asc", limit: Optional[int]=None, offset: Optional[int]=None) -> List[Task]:
        cur = self._conn.cursor()
        # Build dynamic query with filters
        where_clauses = []
        params = []
        if not include_completed:
            where_clauses.append("completed = 0")
        if search:
            where_clauses.append("(title LIKE ? OR description LIKE ?)")
            like_q = f"%{search}%"
            params.extend([like_q, like_q])
        if priority:
            where_clauses.append("priority = ?")
            params.append(priority)
        if tag:
            # simple CSV match
            where_clauses.append("tags LIKE ?")
            params.append(f"%{tag}%")
        if due_before:
            where_clauses.append("due_date <= ?")
            params.append(due_before)
        if due_after:
            where_clauses.append("due_date >= ?")
            params.append(due_after)

        base_query = "SELECT id, title, description, due_date, completed, created_at, priority, tags FROM tasks"
        if where_clauses:
            base_query += " WHERE " + " AND ".join(where_clauses)

        # map sort_by to columns
        sort_map = {
            "due_date": "due_date",
            "created_at": "created_at",
            "priority": "priority",
            "title": "title",
        }
        order_by = sort_map.get(sort_by, "due_date")
        order_clause = "ASC" if order.lower() == "asc" else "DESC"
        base_query += f" ORDER BY {order_by} {order_clause}"

        if limit is not None:
            base_query += " LIMIT ?"
            params.append(limit)
            if offset is not None:
                base_query += " OFFSET ?"
                params.append(offset)

        cur.execute(base_query, tuple(params))
        rows = cur.fetchall()
        return [Task.from_row(r) for r in rows]

    def set_completed(self, task_id: int, completed: bool = True) -> Optional[Task]:
        cur = self._conn.cursor()
        cur.execute("UPDATE tasks SET completed = ? WHERE id = ?", (int(completed), task_id))
        self._conn.commit()
        return self.get_task(task_id)

    def get_task(self, task_id: int) -> Optional[Task]:
        cur = self._conn.cursor()
        cur.execute("SELECT id, title, description, due_date, completed, created_at, priority, tags FROM tasks WHERE id = ?", (task_id,))
        row = cur.fetchone()
        if row is None:
            return None
        return Task.from_row(row)

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass
