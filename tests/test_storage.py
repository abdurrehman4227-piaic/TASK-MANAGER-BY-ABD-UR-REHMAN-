import unittest
import os
from task_manager.storage import SQLiteStorage

class TestStorage(unittest.TestCase):
    def setUp(self):
        # use in-memory database for tests
        self.store = SQLiteStorage(":memory:")

    def tearDown(self):
        self.store.close()

    def test_add_and_get(self):
        t = self.store.add_task("Test task", description="desc")
        self.assertIsNotNone(t.id)
        fetched = self.store.get_task(t.id)
        self.assertEqual(fetched.title, "Test task")
        self.assertEqual(fetched.description, "desc")

    def test_priority_and_tags(self):
        t = self.store.add_task("Priority task", description="pdesc", priority="high", tags="work,urgent")
        self.assertIsNotNone(t.id)
        self.assertEqual(t.priority, "high")
        self.assertListEqual(t.tags, ["work", "urgent"])
        fetched = self.store.get_task(t.id)
        self.assertEqual(fetched.priority, "high")
        self.assertListEqual(fetched.tags, ["work", "urgent"])

    def test_update(self):
        t = self.store.add_task("Old title")
        updated = self.store.update_task(t.id, title="New title", description="Updated desc")
        self.assertIsNotNone(updated)
        self.assertEqual(updated.title, "New title")
        self.assertEqual(updated.description, "Updated desc")

    def test_delete(self):
        t = self.store.add_task("To be deleted")
        ok = self.store.delete_task(t.id)
        self.assertTrue(ok)
        self.assertIsNone(self.store.get_task(t.id))

    def test_complete_toggle(self):
        t = self.store.add_task("Toggle task")
        self.assertFalse(t.completed)
        self.store.set_completed(t.id, True)
        fetched = self.store.get_task(t.id)
        self.assertTrue(fetched.completed)
        self.store.set_completed(t.id, False)
        fetched2 = self.store.get_task(t.id)
        self.assertFalse(fetched2.completed)

    def test_list(self):
        # clear any existing
        a = self.store.add_task("First")
        b = self.store.add_task("Second")
        tasks = self.store.list_tasks()
        self.assertGreaterEqual(len(tasks), 2)

    def test_search_filter_sort(self):
        # setup
        self.store.add_task("Alpha", description="first", priority="low", tags="home")
        self.store.add_task("Beta", description="second", priority="high", tags="work")
        # search
        res = self.store.list_tasks(search="first")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].title, "Alpha")
        # priority filter
        res2 = self.store.list_tasks(priority="high")
        self.assertGreaterEqual(len(res2), 1)
        self.assertEqual(res2[0].priority, "high")
        # tag filter
        res3 = self.store.list_tasks(tag="work")
        self.assertTrue(any("work" in t.tags for t in res3))
        # sort by title asc
        res4 = self.store.list_tasks(sort_by='title', order='asc')
        titles = [t.title for t in res4]
        self.assertEqual(titles, sorted(titles))

if __name__ == '__main__':
    unittest.main()
