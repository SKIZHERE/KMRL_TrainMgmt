# About The Problem and Solution
**1. Start with the Problem (simple story)**

*"Every night, Kochi Metro must decide which trains run, which are kept as backup, and which go for maintenance. Right now, all the information is scattered — in spreadsheets, WhatsApp, and manual logbooks. The managers only get two hours at night to make these choices, which makes it error-prone and stressful.

If they make a mistake, a train might fail in the morning → delays, cost increases, and even revenue loss. As more trains are added, this manual system will break."*

👉 Use real-world examples:

“Imagine they forget to check maintenance → train fails → passengers delayed.”

“Imagine one train is always used → its parts wear faster, costing more.”

**2. Then explain the Solution (our project)**

*"We are building a smart system that takes all this scattered data, applies rules, and gives managers a ranked list of trains that should go into service. The system will also:

Explain why each train is selected.

Alert if there are conflicts (like train not cleaned but scheduled).

Let managers run simulations (‘what if train X is not available?’).

Learn from history to make better forecasts over time."*

**3. Break it into Team Roles (so it’s easy to handle)**

Frontend Dev (newbie):
→ Build simple pages (Login + Dashboard + Table).
→ Don’t worry about logic, just display what backend sends.

Backend Dev (beginner):
→ Handle Flask/FastAPI routes.
→ Connect to rules engine and pass data to frontend.

Python Dev:
→ Write the rules engine (scoring system).
→ Later, improve it with ML.

Java Dev:
→ Build API wrapper (Spring Boot).
→ Make sure frontend can call backend safely.

DBMS Manager:
→ Start with CSV files.
→ Later, move to SQL/DB integration.

UI/UX Designer:
→ Make sure screens are clean, intuitive, and easy for supervisors.
→ Create wireframes/figma mockups.

**4. Wrap it Up with Why it’s Exciting**

"This is not just a coding project — it’s solving a real operational headache. If we succeed, we can reduce costs, improve punctuality, and even build something scalable for other metros in India. Each of us has a clear role, and together we can make a working prototype that looks professional and impactful."



# KMRL_TrainMgmt Prototype

SIH problem 81



---

# 📂 Project Structure (Flask Prototype)

```
kmrl-induction-prototype/
│
├── python-engine/          # Python: logic + scoring engine + Flask backend
│   ├── app.py              # Flask app (login + dashboard)
│   ├── rules_engine.py     # Multi-variable scoring logic
│   ├── ingestion.py        # Load trainset data (CSV/JSON/IoT feeds)
│   ├── data/
│   │   └── trainsets.csv   # Sample data
│   ├── templates/          # HTML templates (Flask Jinja2)
│   │   ├── login.html      # Login page
│   │   └── dashboard.html  # Dashboard (ranked trainsets)
│   └── static/             # Static assets
│       ├── css/
│       │   └── style.css   # Styling
│       └── js/
│           └── app.js      # Optional scripts
│
├── java-service/           # Java: API wrapper / frontend service
│   ├── src/com/kmrl/api/
│   │   ├── ApiServer.java  # Spring Boot starter
│   │   └── TrainsetController.java # REST endpoints (calls Flask)
│   ├── pom.xml             # Maven config
│   └── resources/
│       └── application.properties
│
├── docs/                   # Documentation
│   └── prototype-plan.md
└── README.md               # Overview + setup
```

---

# 🔹 1. Python Engine (Flask)

### `app.py`

* **Purpose**: Flask app, the **core backend**.
* Handles routes like:

  * `/login` → renders login page.
  * `/dashboard` → renders dashboard.
  * `/api/ranked` → returns ranked trainsets (JSON).
  * `/api/simulate` → simulates a trainset’s score.
* **Why Flask?**:

  * Minimal, easy to learn.
  * Integrates naturally with HTML templates (`Jinja2`).
* **Alternatives**:

  * **Django** (too heavy for MVP).
  * **FastAPI** (faster, but less beginner-friendly).
  * Flask chosen → easiest for team’s first prototype.

---

### `rules_engine.py`

* **Purpose**: Contains the **logic for scoring trainsets** (fitness, job card, branding, etc.).
* **Why separate file?**: Keeps business rules independent from Flask routes → makes it modular and testable.
* **Alternatives**: Could keep logic inside `app.py`, but then the code becomes messy.

---

### `ingestion.py`

* **Purpose**: Loads trainset data from `trainsets.csv` or another source.
* **Why**: Separates **data handling** from the logic (clean design).
* **Alternatives**: Could directly hardcode sample data in Python, but then it’s not reusable when switching to DB later.

---

### `data/trainsets.csv`

* **Purpose**: Mock dataset of trainsets.
* **Why CSV?**: Easy for DBMS teammate to work with and modify.
* **Alternatives**:

  * JSON (better for APIs).
  * SQL DB (future).
  * CSV chosen because it’s simplest to start.

---

### `templates/login.html` & `dashboard.html`

* **Purpose**: User-facing pages.
* Rendered by Flask with Jinja2 placeholders.
* **Why Jinja2 templates?**: Allows mixing HTML with dynamic data from Flask.
* **Alternatives**:

  * React/Angular/Vue → heavier, needs separate build pipeline.
  * Plain HTML (no backend data).
  * Jinja chosen for simplicity.

---

### `static/css/style.css`

* **Purpose**: Styles for login + dashboard.
* **Why separate CSS?** Cleaner than inline styles.
* **Alternatives**: Tailwind/Bootstrap (faster prototyping), but plain CSS ensures full control.

---

### `static/js/app.js`

* **Purpose**: Extra frontend scripts (AJAX fetch, event handling).
* **Why optional?**: For prototyping, sometimes enough to use Flask-rendered HTML.

---

# 🔹 2. Java Service (Spring Boot)

### `ApiServer.java`

* **Purpose**: Starts the Spring Boot server (Java wrapper).
* **Why**: Provides APIs for frontend to fetch Python engine results.
* **Alternatives**: Could remove Java and call Flask directly, but then Java dev has no role + less modularity.

---

### `TrainsetController.java`

* **Purpose**: Defines API endpoints in Java:

  * `/api/trainsets/ranked` → calls Flask `/api/ranked`.
  * `/api/trainsets/simulate` → calls Flask `/api/simulate`.
* **Why**: Acts as **middleware** between frontend and Python.
* **Alternatives**:

  * Use Node.js as middleware instead.
  * Skip middleware → but then project loses modularity.

---

### `pom.xml`

* **Purpose**: Maven config for dependencies (Spring Boot, web, JSON).
* **Why Maven?**: Most common Java build tool.
* **Alternative**: Gradle (lighter, newer). Maven chosen → simpler for beginners.

---

# 🔹 3. Docs + README

* **`docs/prototype-plan.md`**: Step-by-step instructions for setup.
* **`README.md`**: Quick overview for new developers.

---

# 🔹 4. Workflow / Data Flow

👉 **How things talk to each other**:

1. **User** → Opens `login.html` → logs in → goes to `dashboard.html`.
2. **Dashboard** → requests data via AJAX.
3. **Java API** → receives request, forwards it to Python Flask.
4. **Python Flask** → applies rules\_engine, fetches data, responds with JSON.
5. **Java API** → sends JSON back to frontend.
6. **Frontend** → updates table/visuals.

---

# 🔹 5. Why this Architecture?

✅ Every team member contributes:

* **Frontend dev** → login, dashboard, CSS.
* **Backend dev** → Flask routes.
* **Java dev** → Spring Boot wrapper.
* **DB dev** → CSV now, real DB later.
* **UI/UX** → styling and flow.
* **Python dev** → rules engine logic.

✅ Prototype looks professional (modular microservices).
✅ Easy to replace components later (e.g., replace CSV with DB).

---




