# GoalFuel (prototype)

GoalFuel is a plain-Java backend prototype for personalized, evidence-backed nutrition recommendations.

Quick start

Build and run the demo that computes nutrition targets:

```bash
mvn -q -DskipTests package
java -cp target/goalfuel-0.1.0-SNAPSHOT.jar com.goalfuel.Main
```

This project contains a simple `NutritionTargetsService` implementation used to compute daily macro targets from a `UserProfile`.
# Nutrition-Advisor