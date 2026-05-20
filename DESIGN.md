**GoalFuel — Design Overview**

Summary
- GoalFuel is a plain-Java backend that produces evidence-based personalized meal recommendations by combining: nutrition-target calculations, a reproducible ranking algorithm, external nutrition/location APIs, and AI-generated explanations (OpenAI).

Scope for this deliverable
- Deliverable: design doc covering requirements, data model, architecture, recommendation scoring, API spec, integration notes, and implementation roadmap.

Tech choices
- Language: Plain Java (Java SE 17+ recommended).
- HTTP layer: lightweight choices — Java HttpServer (built-in) or small microframework (Javalin/Spark) if minimal dependency is acceptable.
- HTTP client: `java.net.http.HttpClient`.
- JSON: `Jackson` or `Gson`.
- Persistence (optional): SQLite/H2 for prototype, or PostgreSQL for production.
- AI: OpenAI (explanations), via REST API; keys kept in environment variables.

High-level architecture
- API Layer: request handling and authentication.
- Domain Services:
  - `UserProfileService` — manages user goals, prefs, restrictions.
  - `NutritionTargetsService` — computes daily/meal targets from user data + research formulas.
  - `RecommendationService` — filters & ranks candidate foods/meals.
  - `NutritionApiClient` — fetches nutrition facts from external provider(s).
  - `LocationService` — finds nearby restaurants/grocers (optional external provider).
  - `AiExplanationService` — calls OpenAI to produce human-friendly rationales.
- Data Layer: DTOs and optional persistence for caching users, foods, and recommendations.

Core domain model (entities)
- `UserProfile`:
  - id, age, sex, heightCm, weightKg, activityLevel, goals (e.g., weight_loss, muscle_gain, maintain), dietaryRestrictions (list), budgetPerMeal, preferences (likes/dislikes), location (lat,lon)
- `NutritionTargets`:
  - caloriesTarget, proteinTargetG, fatTargetG, carbsTargetG, perMealTargets (optional)
- `FoodItem`:
  - id, name, brand, servingSize, priceEstimate, nutrition: {calories, protein_g, fat_g, carbs_g, fiber_g, sodium_mg, sugar_g}, source
- `Meal`:
  - id, name, components: List<FoodItem>, aggregateNutrition, priceEstimate
- `Recommendation`:
  - id, userId, candidateId, score, rankFactors (map), explanationId

Recommendation algorithm (overview)
- Pipeline:
  1. Candidate generation: from local DB, nutrition API search, or nearby restaurants.
  2. Filtering: remove items violating dietaryRestrictions or allergen flags.
  3. Scoring: multi-factor weighted score combining nutrition fit, protein emphasis, preference match, budget match, and distance.

- Scoring formula (normalized components):
  $$score = w_n * N + w_p * P + w_{pref} * Pref + w_b * B + w_d * D$$
  where:
  - $N$ — nutrition fit score (0..1) computed as:
    $$N = 1 - \frac{1}{k}\sum_{i=1}^k \frac{|actual_i - target_i|}{target_i + \epsilon}$$
    (choose targets for calories and macros; clamp values to [0,1])
  - $P$ — protein adequacy bonus (e.g., scaled by grams protein per meal / protein_target_per_meal)
  - $Pref$ — preference match (likes + avoids dislikes)
  - $B$ — budget score (1 if price <= budget else scaled down)
  - $D$ — distance penalty (1 - normalized_distance/maxDistance)
  and weights sum to 1: $w_n + w_p + w_{pref} + w_b + w_d = 1$.

Suggested default weights (tunable): $w_n=0.4, w_p=0.2, w_{pref}=0.15, w_b=0.15, w_d=0.1$.

Evidence & research mapping
- Protein targets: use guidelines such as 1.2–2.0 g/kg/day for active adults; set per-meal target as dailyProtein / mealsPerDay.
- Calorie adjustments: use Mifflin–St Jeor for BMR then multiply by activityFactor and apply target change for weight goals.
- Document which papers or guidelines are used in a README subsection for transparency.

Nutrition API options
- USDA FoodData Central: authoritative, free, good food database.
- Edamam / Nutritionix: easier search endpoints, commercial tiers, may include brands & restaurant menus.
- Design: implement an adapter interface `NutritionApiClient` so you can swap providers.

OpenAI integration (explanations)
- Use OpenAI REST API to generate short explanations describing why a meal was recommended and which targets it helps.
- Example prompt pattern: Provide user profile, meal nutrition summary, and ranked factors; ask for a 2–3 sentence clear explanation with 1-2 evidence-backed bullet points.
- Cache explanation responses keyed by (user profile traits hash + meal id) to reduce calls.

API endpoints (minimal prototype)
- `POST /users` — create/update `UserProfile` (body: user profile JSON)
- `GET /users/{id}/targets` — returns computed `NutritionTargets`
- `POST /search/foods?q=` — search foods via NutritionApiClient (params: q, location?)
- `POST /recommendations` — body: {userId, candidates? , location?} → returns ranked list with scores
- `GET /recommendations/{id}/explanation` — returns cached or newly generated explanation (calls OpenAI if needed)

Security & privacy
- Keep OpenAI and nutrition API keys in environment variables; do not check keys into source control.
- Minimize storage of sensitive PII; store only what’s needed for personalization (consent required).

Testing & evaluation
- Unit tests for targets calculations and scoring components.
- Integration tests mocking NutritionApi and OpenAI responses.
- Offline evaluation: build a dataset of user profiles and ground-truth preferred meals to compute ranking metrics (NDCG, precision@k).

Implementation roadmap (next actions)
1. Implement `UserProfile` and `NutritionTargetsService` (math functions + unit tests).
2. Implement `NutritionApiClient` adapter with a mock provider and one real provider (USDA or Edamam).
3. Implement `RecommendationService` with scoring function and unit tests.
4. Add `AiExplanationService` wrapper for OpenAI and caching.
5. Expose minimal HTTP API and a small CLI or static UI for demo.

Appendix: file & package layout (suggested)
- `src/main/java/com/goalfuel/api` — HTTP handlers
- `src/main/java/com/goalfuel/domain` — entities and DTOs
- `src/main/java/com/goalfuel/service` — services (targets, recommendation, ai)
- `src/main/java/com/goalfuel/integration` — NutritionApiClient, LocationService, OpenAiClient
- `src/test/java/...` — tests

Next step
- I can scaffold a small plain-Java project skeleton (services + DTOs + simple HTTP server) and implement `NutritionTargetsService`. Proceed? 
