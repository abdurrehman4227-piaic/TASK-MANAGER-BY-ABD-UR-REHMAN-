# Task Manager Constitution

## Core Principles & Standards

### 1. Code Quality Standards

#### Code Structure
- **Readability First**: Code must be self-documenting with clear naming conventions
  - Functions: `verb_noun` format (e.g., `create_task`, `validate_input`)
  - Variables: descriptive names avoiding single letters except in loops
  - Classes: PascalCase, nouns describing entities (e.g., `TaskManager`, `UserPreference`)

- **Modularity**: Functions should have single responsibility
  - Maximum function length: 50 lines
  - Each function solves one problem
  - Clear separation of concerns between modules

- **Documentation Requirements**
  - Docstrings for all functions explaining purpose, parameters, and return values
  - Inline comments for complex logic (not obvious what code does)
  - README sections for each major module

#### Code Review Standards
- All changes require review before merge
- Code must pass linting without warnings
- No TODO comments in production code
- Consistent with existing code style in the repository

---

### 2. Testing Standards

#### Test Coverage Requirements
- **Minimum Coverage**: 80% of codebase
- **Critical Paths**: 100% coverage for task operations (CRUD)
- **Edge Cases**: All error conditions must have tests

#### Test Organization
- Test files mirror source structure: `test_module.py` for `module.py`
- Unit tests: Fast, isolated, no external dependencies
- Integration tests: Real data flows, but no real API calls
- Naming: `test_<functionality>` for clarity

#### Test Quality
- Each test verifies one behavior
- Assertions must be specific (not generic true/false checks)
- Tests must be deterministic (no random failures)
- No test interdependencies - tests can run in any order

#### Test Types Required
```
- Unit Tests: Individual functions/methods
- Integration Tests: Module interactions
- Validation Tests: Input validation and error handling
- Performance Tests: Critical operations meet speed requirements
```

---

### 3. User Experience Consistency

#### Interface Consistency
- **Terminology**: Consistent terminology throughout application
  - Task creation always called "Create Task" (not "Add", "New", "Insert")
  - Status values: "Not Started", "In Progress", "Completed"
  - Actions: Verbs in imperative (Create, Delete, Update, View)

- **Navigation**: Predictable, logical flow
  - Primary actions always in same location
  - Error messages appear in consistent place
  - Confirmation dialogs for destructive actions

#### User Feedback Standards
- **Success Messages**: Clear confirmation of action completion
  - Example: "Task created successfully (ID: 12)"
  - Appear consistently for 3-5 seconds

- **Error Messages**: Helpful and actionable
  - Never display raw error codes
  - Explain what went wrong and how to fix it
  - Example: "Task title required. Please enter a task name."

- **Loading States**: Visible feedback for async operations
  - Show spinners/progress for operations > 500ms
  - Disable buttons during processing to prevent duplicates

#### Accessibility Requirements
- Input validation shows errors inline
- Status indicators use color + text (not color alone)
- Response times under 1 second for perceived responsiveness

---

### 4. Performance Requirements

#### Performance Targets
- **Response Time**: User actions receive feedback in < 200ms
- **Data Operations**: 
  - Task CRUD operations: < 100ms
  - Bulk operations (50+ items): < 500ms
  - Search/filter: < 300ms
- **Memory**: Application memory footprint < 100MB
- **Startup**: Application loads in < 2 seconds

#### Performance Standards
- Database queries optimized (no N+1 queries)
- No blocking operations on main thread
- Caching implemented for frequently accessed data
- Resource cleanup after operations (close files, connections)

#### Profiling & Monitoring
- Critical functions logged with execution time
- Performance regression tests for key operations
- Regular profiling to identify bottlenecks
- Benchmark tests establish performance baselines

---

## Implementation Checklist

Every code change must:

- [ ] Follow code quality standards (readable, modular, documented)
- [ ] Include appropriate tests with 80%+ coverage
- [ ] Maintain UI/UX terminology and interaction consistency
- [ ] Meet performance targets for its operation type
- [ ] Pass all existing tests
- [ ] Include updated documentation

## Enforcement

- **Pre-commit Hooks**: Lint and quick style checks
- **CI/CD Pipeline**: Full test suite, coverage reports, performance tests
- **Code Review**: Verify adherence to principles before merge
- **Regular Audits**: Monthly review of code metrics and performance

---

## MVP Feature Specifications

### Foundation Features
These form the foundation—quick to build, essential for any MVP:

#### 1. Add Task
- **Purpose**: Create new todo items
- **Inputs**: Task title (required), description (optional), due date (optional)
- **Output**: Confirmation message with task ID and display in list
- **Validation**: Title cannot be empty, max 255 characters
- **Performance**: Create operation < 100ms
- **UX**: Clear form with inline validation, success confirmation

#### 2. Delete Task
- **Purpose**: Remove tasks from the list
- **Inputs**: Task ID
- **Output**: Confirmation that task was deleted
- **Safety**: Require confirmation dialog to prevent accidental deletion
- **Performance**: Delete operation < 100ms
- **UX**: Consistent destructive action pattern (red color, confirmation required)

#### 3. Update Task
- **Purpose**: Modify existing task details
- **Inputs**: Task ID, updated fields (title, description, due date, priority)
- **Output**: Confirmation with updated task details
- **Validation**: Same as Add Task (title required, length limits)
- **Performance**: Update operation < 100ms
- **UX**: In-place editing or dedicated edit form, clear save/cancel actions

#### 4. View Task List
- **Purpose**: Display all tasks in organized view
- **Features**:
  - Show all task details (title, status, due date, priority)
  - Sort options: by due date, by creation date, by priority, by status
  - Filter options: show active, completed, overdue tasks
  - Search: find tasks by title or description
- **Performance**: Initial load < 500ms, subsequent filters < 300ms
- **UX**: Clear visual hierarchy, status indicators, empty state message when no tasks

#### 5. Mark as Complete
- **Purpose**: Toggle task completion status
- **Inputs**: Task ID, completion status (true/false)
- **Output**: Visual update in list showing completion status
- **Visual Feedback**: Strikethrough or faded appearance for completed tasks
- **Performance**: Toggle operation < 100ms
- **UX**: Single-click/tap action, clear visual change, optional undo option

---

### Intermediate Level (Organization & Usability)

Add these to make the app feel polished and practical:

#### Priorities & Tags/Categories
- **Purpose**: Allow users to express task importance and group related work.
- **Fields**: `priority` (enum: `high`, `medium`, `low`) and `tags` (list of short labels, e.g., `work`, `home`).
- **Model/Storage**: Store `priority` as a constrained string/enum; store `tags` as a normalized relation or as a lightweight delimited field for MVP. Prefer a separate `tags` table when scaling.
- **Validation**: `priority` must be one of allowed values; tags limited to 32 characters and max 10 tags per task.
- **UX**: Show priority as a visible badge (color-coded) and tags as chips; allow quick priority change and tag editing from the task list and edit view; support bulk tag assignment and bulk priority changes.
- **Performance**: Fetching tasks with tag filters should remain < 300ms for typical datasets; consider indexing tag relations and priority columns.

#### Search & Filter
- **Purpose**: Help users quickly find and narrow tasks by keyword and attributes.
- **Capabilities**: Full-text keyword search across title and description; filter by status (active/completed), priority, tags, and date ranges (due before/after).
- **CLI/API**: Provide flags/params such as `--search <query>`, `--status <active|completed>`, `--priority <high|medium|low>`, `--tag <tag>`, `--due-before <date>`, `--due-after <date>`.
- **Implementation**: Use SQLite FTS for text search if available, or simple LIKE queries for MVP. For tags/filters, use indexed columns or join on normalized tag tables.
- **Performance**: Target search/filter response < 300ms for datasets up to 1k tasks; add simple pagination for larger sets.
- **UX**: Provide a prominent search box, immediate filtering with a short debounce (200–300ms), clear active filter chips, and an easy way to clear filters.

#### Sort Tasks
- **Purpose**: Let users reorder results to match their priorities and workflows.
- **Options**: Sort by due date (asc/desc), creation date, priority (high→low), and title (A→Z).
- **Default Behavior**: Default to sorting by due date ascending, then priority descending for tasks with equal dates.
- **Implementation**: Use database ORDER BY for server-side sorting; perform client-side sort only for small result sets (<1k items).
- **Combined Behavior**: Sorting must work together with search and filters and be stable across views.
- **Performance**: Sorting queries should complete < 300ms for expected production datasets; add indexes on sort columns when necessary.


## Definition of Done

A feature or fix is complete only when:

1. ✅ Code passes all quality standards (lint, style, documentation)
2. ✅ Tests written with 80%+ coverage, all passing
3. ✅ UX is consistent with established patterns
4. ✅ Performance meets defined targets
5. ✅ Code reviewed and approved
6. ✅ Documentation updated
7. ✅ No warnings or deprecations introduced
