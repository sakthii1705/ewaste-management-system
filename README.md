# Smart E-Waste Component Recovery and Reuse Management System Using Web Technology

An end-to-end, full-stack web application designed as an **ECE (Electronics & Communication Engineering) Mini Project**. The platform addresses electronic waste accumulation by cataloging decommissioned laboratory devices, harvesting discrete and integrated electronic components, conducting electrical quality testing, matching recovered components to student laboratory projects via intelligent specification normalization, and enforcing transactional stock tracking with public QR code verification certificates.

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, CSS3, JavaScript (ES6+), [Bootstrap 5.3.3](https://getbootstrap.com/), [Bootstrap Icons 1.11](https://icons.getbootstrap.com/), [Chart.js 4.4](https://www.chartjs.org/)
- **Backend:** Python 3.14 / Flask 3.0
- **Database:** MySQL 8.4 Server
- **ORM:** Flask-SQLAlchemy 3.1 (SQLAlchemy 2.0)
- **Authentication & Authorization:** Flask-Login 0.6 with role-based access control (Admin & Student)
- **Security:** Werkzeug password hashing (pbkdf2:sha256), Flask-WTF CSRF protection, secure cookie flags, input validation
- **QR Code Engine:** `qrcode 7.4` and `Pillow 13.0`
- **Testing:** `pytest 8.2` against isolated test database (`ewaste_test_db`)

---

## 📂 Project Architecture

```
ewaste_project/
├── app/
│   ├── blueprints/
│   │   ├── auth.py              # Student registration, login, logout, validation
│   │   ├── main.py              # Public landing page, admin & student dashboards, chart JSON API
│   │   ├── devices.py           # E-waste intake, editing, archival, safe deletion
│   │   ├── components.py        # Inventory CRUD, QR code generation, download
│   │   ├── testing.py           # Quality testing lab, parameter validation, status transitions
│   │   ├── matching.py          # Smart matching engine with spec normalization
│   │   ├── requests.py          # Student requests, admin transactional approval & rejection
│   │   ├── qr.py                # Public read-only QR code verification certificate
│   │   ├── reports.py           # Analytics summary, CSV exports, print-friendly report
│   │   └── users.py             # Admin user authorization & status management
│   ├── services/
│   │   ├── qr_service.py        # QR code image generation with Pillow
│   │   ├── matching_service.py  # Electronics specification normalization & ranking algorithm
│   │   ├── transaction_service.py # Database row-locking (with_for_update) & atomic stock deduction
│   │   └── analytics_service.py # Live SQL aggregation & CSV string generation
│   ├── static/
│   │   ├── css/style.css        # Custom responsive styling and print media rules
│   │   ├── js/main.js           # Client confirmation dialogs and dynamic Chart.js rendering
│   │   └── qr/                  # Generated PNG QR codes for each component
│   ├── templates/
│   │   ├── base.html            # Core layout with sidebar navigation & flash notifications
│   │   ├── home.html            # Public welcome & feature overview landing page
│   │   ├── auth/                # Login & student registration templates
│   │   ├── dashboard/           # Dedicated Admin and Student dashboard views
│   │   ├── devices/             # Device catalog, intake form, and harvested detail view
│   │   ├── components/          # Component inventory, recovery form, and technical details
│   │   ├── testing/             # Testing queue, parameter test form, and testing history
│   │   ├── matching/            # Interactive smart component search interface
│   │   ├── requests/            # Admin review queue, student request form & history
│   │   ├── qr/                  # Public read-only hardware certificate
│   │   ├── reports/             # Analytics overview, transaction ledger, print template
│   │   ├── users/               # Admin user management & role elevation
│   │   └── errors/              # 404, 403, and 500 error pages
│   ├── decorators.py            # @admin_required, audit logging helper
│   ├── extensions.py            # db, login_manager, csrf instances
│   ├── models.py                # Relational SQLAlchemy models and prompt aliases
│   └── __init__.py              # Application factory with context processors & blueprints
├── sql/
│   └── schema.sql               # Relational DDL definitions, CHECK constraints, reference data
├── tests/
│   ├── conftest.py              # Isolated test fixtures using ewaste_test_db
│   ├── test_auth.py             # Registration, login failure, and role authorization tests
│   ├── test_devices.py          # Device CRUD and safe component preservation tests
│   ├── test_components.py       # Inventory CRUD, quantity validation, untested status rule
│   ├── test_testing.py          # Electrical test recording, pass/fail status updates
│   ├── test_matching.py         # Spec normalization, prioritizing reusable, excluding rejected
│   ├── test_requests_transactions.py # Concurrency locking, stock deduction, duplicate prevention
│   ├── test_qr.py               # Public read-only QR verification & download tests
│   └── test_analytics_reports.py# Live DB metric calculation and CSV export tests
├── .env.example                 # Environment variables blueprint
├── .env                         # Local environment configuration
├── config.py                    # Environment configuration classes (Dev, Test, Prod)
├── models.py                    # Root import compatibility re-export
├── seed.py                      # Idempotent demo database seeder
├── run.py                       # Development server runner
├── app.py                       # Application entrypoint
├── requirements.txt             # Locked Python dependencies
└── README.md                    # Project documentation
```

---

## ⚡ Key Features & Engineering Mechanics

### 1. Role-Based Access Control (RBAC)
- **Admin:** Manages intake devices, records salvaged components, operates the Quality Testing Lab, approves/rejects student component requests, manages accounts, and views audit logs.
- **Student:** Browses certified reusable inventory, searches components using the Smart Matching Engine with normalized specifications, submits project component requests, and tracks request statuses in real time.

### 2. Live Database-Driven Admin Dashboard
- **Real-Time KPIs:** Live SQL aggregation of intake devices, component categories, total harvested units, available in-stock inventory, passed reusable parts, untested queue count, rejected parts, and pending requests.
- **Chart.js Visualizations:** Interactive doughnut chart of component category distribution and bar chart of monthly recovery trends fetched via REST endpoint `/api/analytics/charts`.

### 3. Safe E-Waste Intake & Dismantling
- Decommissioned electronic hardware records origin source, model number, received date, disassembly status, and condition notes.
- **Safe Deletion Preservation:** Deleting or archiving a device preserves all recovered component inventory records and historical transactions by safely disassociating foreign key linkages (`ON DELETE SET NULL`), preventing data loss.

### 4. Component Inventory Across 8 Electronic Categories
Supports full technical cataloging for:
1. **Resistors** (Carbon film, metal film, wirewound, SMD)
2. **Capacitors** (Electrolytic, ceramic disc, tantalum, film)
3. **Diodes & LEDs** (1N4007 rectifiers, 1N4148 switching, high-efficiency LEDs)
4. **Transistors** (BJT switching 2N2222, low-noise BC547, power MOSFETs IRF540)
5. **Integrated Circuits (ICs)** (555 timers, 7805 regulators, 741 op-amps, MCUs)
6. **Relays & Switches** (5V PCB relays, slide switches)
7. **Connectors** (Pin headers, terminal blocks)
8. **Sensors & Modules**
- **Strict Quality Rule:** Untested components default to **"Needs Testing"** and are **never** marked reusable automatically upon cataloging.

### 5. Quality Testing Lab & Health Verification
- Admin records electrical test parameters: test method/instrument, expected nominal value, measured value, unit, tolerance percentage, visual inspection, and notes.
- **State Transition Rules:**
  - `result == 'pass'` &rarr; Status becomes **"Reusable"** (certified for academic projects).
  - `result == 'fail'` &rarr; Status becomes **"Rejected"** (quarantined and excluded from usable student searches).
  - Preserves immutable test audit history in `component_tests`.

### 6. Smart Component Matching Engine
- **Specification Normalization:** Resolves varied laboratory notations using regex tokenization:
  - `10k`, `10k ohm`, `10 kohm`, `10000 ohm` &rarr; canonical `10k`
  - `4k7`, `4.7 kohm` &rarr; canonical `4.7k`
  - `100uF`, `100 microfarad`, `100 mfd` &rarr; canonical `100uf`
  - `NE555`, `555 timer` &rarr; canonical `555`
- **Smart Ranking Heuristic:**
  - Prioritizes certified **Reusable** components over untested components.
  - **Excludes rejected components** from usable student matches.
  - Dynamically evaluates requested quantity against live stock, clearly distinguishing between **Stock Sufficient** and **Insufficient Stock (Shortage: X)**.

### 7. Transactional Component Requests & Reuse Ledger
- Students submit component requests specifying quantity, project title, and lab experiment purpose.
- **Concurrency & Stock Integrity:**
  - Approval executes within an atomic database transaction.
  - Employs row-level locking (`SELECT ... FOR UPDATE`) where supported to prevent race conditions.
  - Re-validates stock at the database level and deducts stock **exactly once**.
  - Prevents negative inventory and prohibits duplicate approvals on non-pending requests.
  - Insufficient stock triggers clear feedback without corrupting inventory balance.
  - Creates an audit record and an entry in `stock_transactions` documenting balance after each event.

### 8. QR Code Tracking & Public Read-Only Verification
- Generates high-resolution PNG QR codes using `qrcode` and `Pillow` pointing to `/qr/<component_code>`.
- **Public Certificate:** Mobile scan opens a read-only hardware verification certificate showing component name, rated specs, source device provenance, available quantity, and electrical test status.
- **Security:** Completely unauthenticated access with zero exposure of sensitive user records, passwords, or student identities; no edit actions are permitted via the public endpoint. Allows QR image PNG downloads.

### 9. Analytics, CSV Exports, and Academic Audit Printing
- Computes genuine circular economy metrics: total recovered, total reused, circularity reuse percentage, and category breakdown.
- **CSV Data Exports:**
  - `Export Inventory CSV`: Complete hardware inventory extract.
  - `Export Reuse Ledger CSV`: Transaction ledger of all approved component disbursements.
- **Print View:** Dedicated, print-optimized report (`/reports/print`) formatted with academic department headers, verification blocks, and signature lines for lab instructors and department heads.

---

## 🚀 Setup & Local Execution

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- MySQL 8.0+ running on `localhost:3306`

### 2. Environment Configuration
Verify or edit `.env` in the project root:
```ini
SECRET_KEY=3810240de654cd4b305b1fca5b916f700a9657d951e4a3e2f2900e428c2e73f3
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=ewaste_db
TEST_DB_NAME=ewaste_test_db
FLASK_ENV=development
```

### 3. Database Initialization & Seeding
Run the idempotent seed script to populate demo devices, components across 8 categories in all 3 test states, student and admin accounts, requests, and QR codes:
```powershell
python seed.py
```

### 4. Start the Application Server
Run the Flask application:
```powershell
python run.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🔑 Demo User Credentials

| Role | Email | Password | Access Privileges |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@ewaste.edu` | `Admin@123` | Full control: devices, inventory, quality lab, approvals, reports, user management |
| **Student** | `student@ewaste.edu` | `Student@123` | Smart component search, submit requests, request tracking, student dashboard |
| **Student 2** | `rohan.ece@ewaste.edu` | `Student@123` | Secondary student account for multi-user testing |

---

## 🧪 Automated Test Suite

A comprehensive test suite with 25 unit and integration tests covering all critical paths runs against the isolated test database `ewaste_test_db`:

```powershell
pytest -v
```

### Test Coverage Highlights:
- `test_auth.py`: Student registration, password confirmation, validation rules, login failure handling, role-based route protection.
- `test_devices.py`: Device intake, updates, and safe deletion ensuring inventory components remain preserved.
- `test_components.py`: Component cataloging, quantity positive validation, and strict default untested rule enforcement.
- `test_testing.py`: Recording electrical test records, passing test transition to Reusable, failing test transition to Rejected.
- `test_matching.py`: Specification normalization, ranking reusable over untested, excluding rejected parts, flagging stock shortage.
- `test_requests_transactions.py`: Student request submission, transactional approval with row-locking, stock deduction, duplicate prevention, insufficient stock error handling.
- `test_qr.py`: Public read-only QR verification without authentication, privacy protection (no password leaks), QR image download.
- `test_analytics_reports.py`: Live database KPI computation, inventory CSV export, and reuse ledger CSV export.

---

## 📄 Academic Project Attribution
- **Project Title:** Smart E-Waste Component Recovery and Reuse Management System Using Web Technology
- **Department:** Electronics & Communication Engineering (ECE)
- **Course Level:** Medium-Level ECE Mini Project
- **Domain:** Web Technology, Database Engineering, Hardware Resource Circularity
