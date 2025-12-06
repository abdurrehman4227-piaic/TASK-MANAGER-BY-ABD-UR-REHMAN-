#!/usr/bin/env python3
import argparse
from task_manager.storage import SQLiteStorage

DB_PATH = "tasks.db"

def cmd_add(args):
    store = SQLiteStorage(DB_PATH)
    task = store.add_task(args.title, description=args.description, due_date=args.due, priority=args.priority, tags=args.tags)
    print(f"Task created successfully (ID: {task.id})")
    store.close()

def cmd_delete(args):
    store = SQLiteStorage(DB_PATH)
    ok = store.delete_task(args.id)
    if ok:
        print(f"Task {args.id} deleted")
    else:
        print(f"Task {args.id} not found")
    store.close()

def cmd_update(args):
    store = SQLiteStorage(DB_PATH)
    task = store.update_task(args.id, title=args.title, description=args.description, due_date=args.due, priority=args.priority, tags=args.tags)
    if task:
        print(f"Task {task.id} updated")
    else:
        print(f"Task {args.id} not found")
    store.close()

def cmd_list(args):
    store = SQLiteStorage(DB_PATH)
    limit = args.limit if hasattr(args, 'limit') and args.limit is not None else None
    page = args.page if hasattr(args, 'page') and args.page and args.page > 0 else 1
    offset = (page - 1) * limit if limit else None
    tasks = store.list_tasks(
        include_completed=not args.active,
        search=getattr(args, 'search', None),
        priority=getattr(args, 'priority', None),
        tag=getattr(args, 'tag', None),
        due_before=getattr(args, 'due_before', None),
        due_after=getattr(args, 'due_after', None),
        sort_by=getattr(args, 'sort', 'due_date'),
        order=getattr(args, 'order', 'asc'),
        limit=limit,
        offset=offset,
    )
    if not tasks:
        print("No tasks found")
    else:
        # simple colored priority badge
        color_map = {"high": "\x1b[31m", "medium": "\x1b[33m", "low": "\x1b[32m"}
        reset = "\x1b[0m"
        for t in tasks:
            status = "✔" if t.completed else " "
            tags_disp = f" [{', '.join(t.tags)}]" if getattr(t, 'tags', None) else ""
            color = color_map.get(getattr(t, 'priority', 'medium'), "")
            pr_disp = f"{color}{t.priority}{reset}"
            print(f"[{status}] {t.id}: {t.title} (due: {t.due_date}) priority={pr_disp}{tags_disp}")
    store.close()

def cmd_complete(args):
    store = SQLiteStorage(DB_PATH)
    task = store.set_completed(args.id, completed=True)
    if task:
        print(f"Task {args.id} marked completed")
    else:
        print(f"Task {args.id} not found")
    store.close()

def cmd_uncomplete(args):
    store = SQLiteStorage(DB_PATH)
    task = store.set_completed(args.id, completed=False)
    if task:
        print(f"Task {args.id} marked active")
    else:
        print(f"Task {args.id} not found")
    store.close()


def main():
    parser = argparse.ArgumentParser(prog="task-manager")
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add")
    p_add.add_argument("title")
    p_add.add_argument("--description", "-d", default=None)
    p_add.add_argument("--due", default=None)
    p_add.add_argument("--priority", choices=["high", "medium", "low"], default="medium")
    p_add.add_argument("--tags", default=None, help="comma-separated tags e.g. work,home")
    p_add.set_defaults(func=cmd_add)

    p_delete = sub.add_parser("delete")
    p_delete.add_argument("id", type=int)
    p_delete.set_defaults(func=cmd_delete)

    p_update = sub.add_parser("update")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--title", default=None)
    p_update.add_argument("--description", default=None)
    p_update.add_argument("--due", default=None)
    p_update.add_argument("--priority", choices=["high", "medium", "low"], default=None)
    p_update.add_argument("--tags", default=None, help="comma-separated tags e.g. work,home")
    p_update.set_defaults(func=cmd_update)

    p_list = sub.add_parser("list")
    p_list.add_argument("--active", action="store_true", help="show only active tasks")
    p_list.add_argument("--search", default=None, help="search keyword in title/description")
    p_list.add_argument("--priority", choices=["high", "medium", "low"], default=None)
    p_list.add_argument("--tag", default=None, help="filter by tag")
    p_list.add_argument("--due-before", dest="due_before", default=None)
    p_list.add_argument("--due-after", dest="due_after", default=None)
    p_list.add_argument("--sort", choices=["due_date", "created_at", "priority", "title"], default="due_date")
    p_list.add_argument("--order", choices=["asc", "desc"], default="asc")
    p_list.add_argument("--limit", type=int, default=None, help="number of items per page")
    p_list.add_argument("--page", type=int, default=1, help="page number (starts at 1)")
    p_list.set_defaults(func=cmd_list)

    p_complete = sub.add_parser("complete")
    p_complete.add_argument("id", type=int)
    p_complete.set_defaults(func=cmd_complete)

    p_uncomplete = sub.add_parser("uncomplete")
    p_uncomplete.add_argument("id", type=int)
    p_uncomplete.set_defaults(func=cmd_uncomplete)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
