## Design Report

### Architecture Overview

#### Modular Structure

- **formulator**: Converts database schema into HTML forms and CRUD views.
- **templeton**: Template engine wrapping Flask views into standard layouts.
- **safeHaven**: Route protection and authentication decorators.
- **toolkit**: Utility functions for route registration, DB I/O, and schema parsing.

#### Blueprint-Based Routing

Each module can be loaded as a Flask Blueprint, allowing independent development and integration. Navigation, view registration, and auth middleware are initialized at the application level.

### Technology Stack

- Flask
- MySQL
- Jinja2
- Python

### Data Flow

#### Directory Structure
```plaintext
/interlink/src/interlink
├── formulator
│   ├── __init__.py
│   └── logic.py
├── __init__.py
├── __main__.py
├── safeHaven
│   └── __init__.py
├── templeton
│   ├── __init__.py
│   ├── templates
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── admin.html
│   │   ├── copyright.html
│   │   ├── data.html
│   │   ├── forms.html
│   │   ├── guide
│   │   │   └── index.html
│   │   ├── login.html
│   │   ├── nav.html
│   │   ├── reports.html
│   │   ├── template.html
│   │   └── templeton.html
│   └── views.py
└── toolkit
    └── __init__.py
```

- **Diagram – Module Interaction**
```
  ┌─────────────┐    ┌──────────────┐
  │  formulator │───▶│   templeton  │
  └─────────────┘    └──────────────┘
         │                   │
         ▼                   ▼
  ┌─────────────┐    ┌──────────────┐
  │  safeHaven  │    │   toolkit    │
  └─────────────┘    └──────────────┘
```

### UI/UX Design
A minimal UI approach is taken by default, but templates are overrideable using Jinja2 template inheritance. Menus and layouts are dynamically generated based on the database schema and user permissions.

### Security Considerations

- Currently optimized for MySQL. PostgreSQL and SQLite support planned.
- Tight coupling to Flask—porting to FastAPI would require wrapper layers.

### Scalability Plan

- Plugin system for frontend themes
- Admin dashboard with configurable widgets
- CLI scaffolding for new project generation
