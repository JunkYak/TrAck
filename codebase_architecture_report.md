# trAck Codebase Deep Architecture Audit & Handoff Report

## Section 1 — Project Overview

**trAck** is a minimalist tracking application designed to help users log their Nutrition, Health, and Training data without the noise of complex analytics, AI recommendations, or streak systems. 

**Core Philosophy:**
- **Simplicity & Speed:** The primary objective of trAck is to allow users to quickly log their daily data. 
- **Domain Separation:** Clean boundaries between raw data entry and future analytics layers.
- **No Workout Sessions:** Training focuses on a "master catalogue" of exercises and weekly best sets, avoiding the overhead of tracking every single rep, set, or rest timer.
- **Minimalist UI:** High emphasis on readability, consistent "completion states" using color logic (Grey = Empty, Color = Filled), and sleek micro-animations.

**Current Implemented Domains:**
- **Nutrition:** Foods (library), Recipes (combinations of foods), Templates (saved meal structures), Kitchen (daily logging).
- **Health:** Weight tracking, Measurement sessions (Waist, Bicep, Quad).
- **Training:** Exercise library (best sets per week), Cardio tracking (distance, duration, pace).
- **Dashboard:** A unified hub with status cards acting as primary navigation.

**Technology Stack:**

**Frontend:**
- **Framework:** React 18+ (via Vite)
- **Language:** TypeScript
- **State/Data Fetching:** React Query (TanStack Query) for asynchronous state, local caching, and invalidation.
- **Form Management:** React Hook Form for performant, uncontrolled form validation.
- **Styling:** Tailwind CSS for utility-first styling.
- **UI Components:** Radix UI primitives (e.g., Dialogs) for accessible, unstyled structural components.
- **Charts:** Recharts for minimal trend visualization.

**Backend:**
- **Framework:** FastAPI (Python 3.10+)
- **Language:** Python
- **ORM:** SQLAlchemy 2.0 (using `Mapped` and `mapped_column` patterns).
- **Migrations:** Alembic
- **Database:** SQLite (local development), planned migration to PostgreSQL for production.
- **Architecture:** Async, layered architecture (Router → Service → Repository → DB).

**Deployment Target:**
- **Frontend:** Vercel
- **Backend:** Azure App Service / Azure Container Apps
- **Database:** SQLite (currently), Azure Database for PostgreSQL (planned).
- **Auth:** Google OAuth (planned).

---

## Section 2 — Complete Folder Tree

```text
frontend/
├── src/
│   ├── app/
│   │   ├── queryClient.ts
│   │   └── router.tsx
│   ├── features/
│   │   ├── dashboard/
│   │   │   └── pages/
│   │   │       └── DashboardPage.tsx
│   │   ├── health/
│   │   │   ├── api/
│   │   │   │   ├── measurements.ts
│   │   │   │   └── weight.ts
│   │   │   ├── pages/
│   │   │   │   ├── MeasurementsPage.tsx
│   │   │   │   └── WeightPage.tsx
│   │   │   └── types/
│   │   │       └── index.ts
│   │   ├── nutrition/
│   │   │   ├── api/
│   │   │   │   └── nutrition.ts
│   │   │   ├── components/
│   │   │   │   ├── Foods/
│   │   │   │   ├── Kitchen/
│   │   │   │   ├── Recipes/
│   │   │   │   ├── Shared/
│   │   │   │   └── Templates/
│   │   │   ├── layouts/
│   │   │   │   └── NutritionWorkspaceLayout.tsx
│   │   │   ├── pages/
│   │   │   │   ├── FoodsPage.tsx
│   │   │   │   ├── KitchenPage.tsx
│   │   │   │   ├── RecipesPage.tsx
│   │   │   │   └── TemplatesPage.tsx
│   │   │   ├── types/
│   │   │   │   └── index.ts
│   │   │   └── utils/
│   │   │       ├── nutritionCalculations.ts
│   │   │       └── templateCalculations.ts
│   │   └── training/
│   │       ├── api/
│   │       │   ├── cardio.ts
│   │       │   └── exercises.ts
│   │       ├── pages/
│   │       │   ├── CardioPage.tsx
│   │       │   └── ExerciseLibraryPage.tsx
│   │       ├── types/
│   │       │   └── index.ts
│   │       └── utils/
│   │           ├── date.ts
│   │           └── format.ts
│   ├── hooks/
│   │   └── useDebounce.ts
│   ├── layouts/
│   │   └── GlobalWorkspaceLayout.tsx
│   ├── lib/
│   │   └── axios.ts
│   ├── index.css
│   └── main.tsx

backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── cardio.py
│   │       ├── exercises.py
│   │       ├── foods.py
│   │       ├── health.py
│   │       ├── meal_templates.py
│   │       ├── measurements.py
│   │       ├── nutrition_logs.py
│   │       ├── recipes.py
│   │       ├── router.py
│   │       └── weights.py
│   ├── auth/
│   │   ├── oauth.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   └── security.py
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── cardio.py
│   │   ├── exercise.py
│   │   ├── exercise_log.py
│   │   ├── food_item.py
│   │   ├── meal_template.py
│   │   ├── measurement_session.py
│   │   ├── nutrition_log.py
│   │   ├── recipe.py
│   │   ├── user.py
│   │   └── weight_log.py
│   ├── repositories/
│   │   ├── base.py
│   │   ├── cardio.py
│   │   ├── exercise.py
│   │   ├── exercise_log.py
│   │   ├── food_item.py
│   │   ├── meal_template.py
│   │   ├── measurement_session.py
│   │   ├── nutrition_log.py
│   │   ├── recipe.py
│   │   ├── user.py
│   │   └── weight_log.py
│   ├── schemas/
│   │   ├── cardio.py
│   │   ├── common.py
│   │   ├── exercise.py
│   │   ├── exercise_log.py
│   │   ├── food_item.py
│   │   ├── meal_template.py
│   │   ├── measurement_session.py
│   │   ├── nutrition_log.py
│   │   ├── recipe.py
│   │   ├── user.py
│   │   └── weight_log.py
│   ├── services/
│   │   ├── base.py
│   │   ├── cardio.py
│   │   ├── exercise.py
│   │   ├── exercise_log.py
│   │   ├── food_item.py
│   │   ├── meal_template.py
│   │   ├── measurement_session.py
│   │   ├── nutrition_log.py
│   │   ├── recipe.py
│   │   ├── user.py
│   │   └── weight_log.py
│   ├── main.py
│   └── __init__.py
```

---

## Section 3 — File By File Explanation

### Frontend Significant Files

#### `frontend/src/app/router.tsx`
- **Purpose:** Central routing configuration using `react-router-dom`.
- **Inputs:** None.
- **Outputs:** Exposes the `<RouterProvider>` containing all application routes.
- **Dependencies:** React Router, `GlobalWorkspaceLayout`, Feature Pages (Dashboard, Kitchen, Weight, etc.).
- **Used By:** `frontend/src/main.tsx`
- **Lifecycle:** Mounts the layout shell and injects the corresponding feature page into the `<Outlet />` based on the URL.

#### `frontend/src/features/dashboard/pages/DashboardPage.tsx`
- **Purpose:** The primary hub and navigation center of the app.
- **Inputs:** Route mount.
- **Outputs:** Renders the 5 status cards (Nutrition, Weight, Measurements, Strength, Cardio).
- **Dependencies:** Domain APIs (e.g., `useDailyLog`, `useLatestWeight`), React Router `NavLink`.
- **Used By:** `router.tsx`
- **Lifecycle:** Mounts → Triggers 5 separate React Query hooks to fetch the latest status for each domain → Calculates empty/filled states → Renders colored interactive cards.

#### `frontend/src/features/nutrition/pages/KitchenPage.tsx`
- **Purpose:** The daily nutrition logging interface.
- **Inputs:** Selected date (currently defaults to today).
- **Outputs:** Renders the `NutritionSummaryCard`, the list of logged entries, and the `AddLogInlinePanel` to add new foods/recipes.
- **Dependencies:** `useDailyLog` hook, Kitchen components (`NutritionSummaryCard`, `LoggedEntryGroup`).
- **Used By:** `router.tsx`
- **Lifecycle:** Mounts → Fetches today's nutrition log → Renders entries. When a user adds an item, it calls a mutation which invalidates the log query, causing a re-render.

#### `frontend/src/features/nutrition/api/nutrition.ts`
- **Purpose:** Centralized API interactions for the Nutrition domain.
- **Inputs:** DTOs from components.
- **Outputs:** React Query hooks (`useFoods`, `useCreateFood`, `useDailyLog`, etc.).
- **Dependencies:** `axios.ts` (API client), `@tanstack/react-query`.
- **Used By:** `KitchenPage.tsx`, `FoodsPage.tsx`, etc.
- **Lifecycle:** Components call these hooks. Mutations trigger backend requests and on success, explicitly invalidate the `nutritionKeys` cache to trigger refetches.

### Backend Significant Files

#### `app/main.py`
- **Purpose:** Application entry point.
- **Inputs:** ASGI server startup.
- **Outputs:** The FastAPI `app` instance.
- **Dependencies:** `app.api.v1.router`, `app.core.config`, `fastapi.middleware.cors`.
- **Used By:** Uvicorn.
- **Lifecycle:** Initializes FastAPI → Configures CORS → Mounts the API v1 router.

#### `app/api/v1/router.py`
- **Purpose:** Aggregates all v1 domain routers.
- **Inputs:** Requests to `/api/v1/*`.
- **Outputs:** Routes requests to specific domain files (e.g., `foods.py`, `weights.py`).
- **Dependencies:** FastAPI `APIRouter`, domain router modules.
- **Used By:** `main.py`
- **Lifecycle:** Registers prefixes (`/foods`, `/weights`) and delegates handling.

#### `app/services/base.py` & `app/repositories/base.py`
- **Purpose:** Generic Base Repository and Service classes providing standard CRUD operations.
- **Inputs:** SQLAlchemy models, schemas.
- **Outputs:** Instantiated generic methods (`get`, `create`, `update`, `delete`).
- **Dependencies:** SQLAlchemy `Session`.
- **Used By:** All specific domain services/repositories.
- **Lifecycle:** Provides the foundation for the Service/Repo layer. Specific domains inherit from these and add custom business logic.

#### `app/models/nutrition_log.py`
- **Purpose:** Defines the schema for `DailyNutritionLog`, `DailyNutritionLogEntry`, and `DailyNutritionLogItem`.
- **Inputs:** SQLAlchemy Base.
- **Outputs:** Database table mappings.
- **Dependencies:** `app.database.base`.
- **Used By:** Repositories, Alembic.
- **Lifecycle:** Used by SQLAlchemy to execute CRUD operations and manage relationships (one log → many entries → many items).

---

## Section 4 — Frontend Architecture

The frontend follows a strictly modular, feature-based architecture.

**Routing & Layouts:**
- Managed by `react-router-dom`.
- `GlobalWorkspaceLayout` provides the persistent sidebar navigation and a main content area (`<Outlet />`).
- Features are strictly siloed in `src/features/`.

**State Management & API Layer:**
- **Asynchronous State:** `@tanstack/react-query` handles all server state. Custom hooks (e.g., `useFoods`) wrap Axios calls.
- **Cache Invalidation:** Mutations cleanly invalidate specific query keys (e.g., `queryClient.invalidateQueries({ queryKey: nutritionKeys.foods() })`) ensuring UI consistency without manual state syncing.
- **Forms:** `react-hook-form` manages form state to prevent unnecessary re-renders.

**Feature Domains:**
- **Nutrition (`/nutrition`):**
  - Divided into Kitchen (daily logging), Foods (custom food DB), Recipes (grouped foods), and Templates.
  - Highly interactive forms utilizing Dialogs.
- **Health (`/health`):**
  - Contains Weight and Measurements.
  - Utilizes Recharts for simple line graphs mapping progress over time.
- **Training (`/training`):**
  - Contains Exercises (master catalogue + weekly best sets) and Cardio.
  - UI relies heavily on calculating dates (e.g., `getStartOfWeekDate()`) to enforce the "one best set per week" domain rule.
- **Dashboard (`/dashboard`):**
  - Aggregates the `useLatest...` hooks from all domains.
  - Enforces strict UI "Completion States" (Grey = Empty, Colored = Populated). Cards act as full `<NavLink>` wrappers.

**Interaction Diagram (Logging a weight):**
```text
WeightPage.tsx (User clicks "Log Weight")
→ weight.ts (useCreateWeight hook triggers mutation)
→ axios.ts (POST /api/v1/weights)
→ FastAPI (receives request)
→ React Query onSuccess (Invalidates weightKeys)
→ WeightPage.tsx & DashboardPage.tsx (Re-renders with new weight)
```

---

## Section 5 — Backend Architecture

The backend implements a strict Layered Architecture to decouple routing, business logic, and database access.

**Layers:**
1. **API Layer (`app/api/v1/`):** FastAPI routers. Defines endpoints, injects dependencies (DB session, current user), parses request schemas, and returns response schemas.
2. **Service Layer (`app/services/`):** Contains pure business logic. Enforces ownership rules, validation rules (e.g., "only one weight per day"), and orchestration.
3. **Repository Layer (`app/repositories/`):** Handles raw SQLAlchemy queries. Keeps SQLAlchemy logic completely isolated from Services.
4. **Database Layer (`app/models/`):** SQLAlchemy ORM models defining exact table schemas.

**Schemas (DTOs):** Pydantic models (`app/schemas/`) strictly validate incoming requests (Create/Update) and format outgoing responses (Read).

**Error Handling:** Managed via `HTTPException`. Services raise exceptions (e.g., 404 Not Found, 403 Forbidden) which FastAPI catches and formats.

**Dependency Injection:** Every router endpoint accepts `db: Session = Depends(get_db)` and `current_user_id: str = Depends(get_current_user_id)`.

**Request Flow Example (Logging Cardio):**
```text
Request (POST /api/v1/cardio)
→ Router (app/api/v1/cardio.py : create_session)
→ Injects db, user_id, parses CardioSessionCreate DTO
→ Service (CardioService.create)
→ Calculates average_pace and estimated_calories natively
→ Repository (CardioRepository.create)
→ Database (INSERT INTO cardio_sessions)
→ Response (CardioSessionRead DTO via Router)
```

---

## Section 6 — Database Architecture

All models inherit from `app.database.base.Base`. Every table uses a UUID `id` and a UUID `user_id`.

**1. Users (`users`)**
- **Purpose:** Core user account.
- **Columns:** `id`, `google_id`, `email`, `name`, `profile_picture`, `created_at`.

**2. Foods (`food_items`)**
- **Purpose:** Master catalogue of user-created foods.
- **Columns:** `id`, `user_id`, `name`, `brand_name`, `calories_per_unit`, `protein_per_unit`, `carbs_per_unit`, `fat_per_unit`, `unit`.

**3. Recipes (`recipes`) & Recipe Ingredients (`recipe_ingredients`)**
- **Purpose:** Reusable combinations of foods.
- **Columns (Recipes):** `id`, `user_id`, `name`, `prep_time_minutes`.
- **Columns (Ingredients):** `id`, `recipe_id` (FK), `food_item_id` (FK), `quantity`.
- **Relationships:** A Recipe has many RecipeIngredients. Each Ingredient links to a FoodItem.

**4. Meal Templates (`meal_templates`), Template Foods, Template Recipes**
- **Purpose:** Named meals containing foods and recipes for 1-click logging.
- **Relationships:** A Template maps to multiple `MealTemplateFood` and `MealTemplateRecipe` junction tables.

**5. Nutrition Logs (`daily_nutrition_logs`, `daily_nutrition_log_entries`, `daily_nutrition_log_items`)**
- **Purpose:** The daily diary of consumed nutrition.
- **Architecture:** 
  - `DailyNutritionLog` (1 per date per user).
  - `DailyNutritionLogEntry` (Groupings like "Breakfast" or "Whey Protein").
  - `DailyNutritionLogItem` (The actual raw foods inside that entry).
- **Relationships:** Log → Entries → Items.

**6. Weight Logs (`weight_logs`)**
- **Purpose:** Daily body weight.
- **Columns:** `id`, `user_id`, `date`, `weight_kg`.
- **Constraints:** Unique constraint on `(user_id, date)`. Upsert logic applied.

**7. Measurement Sessions (`measurement_sessions`)**
- **Purpose:** Weekly body measurements.
- **Columns:** `id`, `user_id`, `date`, `waist_in`, `bicep_in`, `quad_in`.
- **Constraints:** Unique on `(user_id, date)`.

**8. Exercises (`exercises`) & Exercise Logs (`exercise_logs`)**
- **Purpose:** Master catalogue of exercises and weekly best-set tracking.
- **Columns (Exercises):** `id`, `user_id`, `name`, `category`.
- **Columns (Logs):** `id`, `user_id`, `exercise_id` (FK), `log_date`, `weight_kg`, `reps`.

**9. Cardio Sessions (`cardio_sessions`)**
- **Purpose:** Logging runs/cardio.
- **Columns:** `id`, `user_id`, `performed_at`, `run_type` (Enum: EASY, TEMPO_INTERVAL, LONG), `distance_km`, `duration_minutes`, `average_pace`, `estimated_calories`.

---

## Section 7 — Domain Walkthroughs

### Health (Weight Example)
- **User Workflow:** User opens Dashboard, clicks Weight Card, enters "76" for today, clicks Save.
- **Frontend Flow:** `WeightPage` calls `useCreateWeight` → POST `/api/v1/weights` with `{"date": "2026-06-18", "weight_kg": 76}`.
- **Backend Flow:** Router receives payload. `WeightLogService` checks if a log exists for today. If yes, it updates it. If no, it creates it (Upsert pattern).
- **Database Flow:** `UPDATE weight_logs` or `INSERT INTO weight_logs`.
- **Data Lifecycle:** React Query invalidates `weightKeys`, triggering the `DashboardPage` and `WeightPage` trend charts to instantly render the new data point.

### Training (Cardio Example)
- **User Workflow:** User logs a 10km run in 58 minutes.
- **Frontend Flow:** Form maps "Tempo Run" UI button to `TEMPO_INTERVAL` Enum. Submits to `/api/v1/cardio`.
- **Backend Flow:** Service intercepts payload. Calculates `average_pace` (5.8 mins/km) and `estimated_calories`. 
- **Database Flow:** Inserts new session.
- **Frontend Lifecycle:** UI receives backend response, invalidates cache. A local utility `formatPace` converts the `5.8` float into a string `"5:48/km"` for display.

---

## Section 8 — Current Features

**Nutrition Domain**
- **Foods:** (Status: Complete) Create, read, update, delete custom food items.
- **Recipes:** (Status: Complete) Aggregate multiple foods into a single entity.
- **Templates:** (Status: Complete) Group foods and recipes for 1-click logging.
- **Kitchen:** (Status: Complete) The daily log. Calculates macros on the fly. 

**Health Domain**
- **Weight:** (Status: Complete) Daily logging with upsert logic. Trend charts implemented.
- **Measurements:** (Status: Complete) Weekly tracking of Waist, Bicep, Quad. Trend charts implemented.

**Training Domain**
- **Exercises:** (Status: Complete) Master catalogue of exercises. Weekly best set logging implemented. Does NOT support workout sessions or volume tracking.
- **Cardio:** (Status: Complete) Distance, duration, pace tracking. Enforces Enum validation.

**Dashboard Domain**
- **Status Cards:** (Status: Complete) 5 distinct cards (Nutrition, Weight, Measurements, Strength, Cardio). Fully clickable, highly responsive, with strict empty/filled visual states.

---

## Section 9 — Authentication Status

- **Current State:** The application is completely decoupled from authentication in development. 
- **Mechanism:** `app.core.security` provides a `get_current_user_id` dependency that currently hardcodes a mock UUID (`_DEV_TEST_USER_ID = "00000000-0000-0000-0000-000000000001"`).
- **User Model:** The `User` table exists and is seeded with the mock UUID.
- **Ownership Enforcement:** EVERY service and repository explicitly filters by `user_id`. Multi-tenancy is technically fully implemented; it simply lacks the token parser.
- **Planned:** Google OAuth integration. 
- **Session Strategy Recommendations:** Use HTTP-only secure cookies containing a JWT for session persistence to avoid local storage vulnerabilities.

---

## Section 10 — Deployment Status

- **Current Local Architecture:** Node (Vite/React) on `localhost:5173`. Uvicorn (FastAPI) on `localhost:8000`. SQLite file (`track.db`) located in backend root. Vite proxies `/api` to `localhost:8000`.
- **Planned Production Architecture:**
  - **Frontend:** Vercel (Requires setting Vite proxy rules or rewriting Vercel API routes to hit the Azure domain).
  - **Backend:** Azure App Service or Azure Container Apps (Dockerized).
  - **Database:** Azure Database for PostgreSQL.
- **Environment Variables:** Currently absent. Need `.env` for `DATABASE_URL`, `GOOGLE_CLIENT_ID`, `FRONTEND_URL`.
- **Risks:** Alembic migrations are currently tailored to SQLite. Migrating to PostgreSQL will require minor schema adjustments (e.g., ensuring Enums are handled properly in PG).

---

## Section 11 — Known Technical Debt & Future Opportunities

**High Priority:**
1. **Google OAuth Integration:** The hardcoded user ID must be replaced before deployment.
2. **PostgreSQL Migration:** SQLite is not suitable for Vercel/Azure stateless deployments. Alembic must be pointed to a PG instance.

**Medium Priority:**
1. **Vercel & Azure Deployment:** Setup CI/CD pipelines, configure CORS properly for the production domains.
2. **Skeleton Loaders:** Replace plain text "Loading..." states with UI skeletons to prevent layout shift during React Query fetching.
3. **PWA Support:** Add a Web App Manifest and Service Worker to allow users to install trAck to their iOS/Android home screens, removing browser chrome.

**Low Priority / Future Features:**
1. **Analytics Layer:** A dedicated section for monthly/yearly trend reviews (strictly separated from the daily entry views).
2. **AI Nutrition Autofill:** Parsing natural language ("I ate 2 eggs and a piece of toast") into the Kitchen log.

---

## Section 12 — Developer Handoff Summary

Welcome to trAck!

**How it works:** trAck is a React + FastAPI app designed for minimal friction tracking. It avoids complex session building (no sets/reps trackers, no GPS tracking) in favor of simple daily/weekly aggregates.
**Where to find functionality:**
- Frontend features are strictly siloed in `frontend/src/features/[domain]`.
- Backend endpoints map directly to `app/api/v1/[domain].py` and flow down through `services/` to `repositories/`.
**How data flows:** UI interactions trigger React Query Mutations → FastAPI updates SQLite → React Query invalidates cache → UI re-renders automatically.
**What is complete:** The entire core functionality of all 4 domains (Nutrition, Health, Training, Dashboard) is fully implemented, styled, and audited. Data ownership constraints are embedded in the backend.
**What remains:** Authentication (Google OAuth), Production Deployment (Azure/Vercel), and migrating the database engine from SQLite to PostgreSQL. The codebase is remarkably clean, tightly coupled to its domain philosophy, and ready for production scaffolding.
