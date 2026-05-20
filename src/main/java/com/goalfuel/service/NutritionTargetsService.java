package com.goalfuel.service;

import com.goalfuel.domain.NutritionTargets;
import com.goalfuel.domain.UserProfile;

public class NutritionTargetsService {

    // Compute BMR using Mifflin-St Jeor
    public double computeBMR(UserProfile u) {
        double weight = u.getWeightKg();
        double height = u.getHeightCm();
        int age = u.getAge();
        if ("male".equalsIgnoreCase(u.getSex())) {
            return 10 * weight + 6.25 * height - 5 * age + 5;
        } else {
            return 10 * weight + 6.25 * height - 5 * age - 161;
        }
    }

    // Activity multiplier mapping
    public double activityFactor(UserProfile u) {
        switch (u.getActivityLevel().toLowerCase()) {
            case "sedentary": return 1.2;
            case "light": return 1.375;
            case "moderate": return 1.55;
            case "active": return 1.725;
            case "very_active": return 1.9;
            default: return 1.2;
        }
    }

    // Protein grams per kg mapping by goal
    public double proteinPerKg(UserProfile u) {
        switch (u.getGoal().toLowerCase()) {
            case "muscle_gain": return 1.6; // g/kg
            case "weight_loss": return 1.4;
            case "maintain": return 1.2;
            default: return 1.2;
        }
    }

    public NutritionTargets computeTargets(UserProfile u) {
        double bmr = computeBMR(u);
        double calories = bmr * activityFactor(u);

        // Adjust calories for goals (simple heuristic)
        if ("weight_loss".equalsIgnoreCase(u.getGoal())) {
            calories -= 500; // moderate deficit
        } else if ("muscle_gain".equalsIgnoreCase(u.getGoal())) {
            calories += 300; // small surplus
        }
        if (calories < 1200) calories = 1200; // floor

        double proteinG = proteinPerKg(u) * u.getWeightKg();

        // Fat target: ~25% of calories, 9 kcal/g
        double fatCalories = 0.25 * calories;
        double fatG = fatCalories / 9.0;

        // Protein calories
        double proteinCalories = proteinG * 4.0;

        // Carbs calories: remainder
        double carbsCalories = calories - (proteinCalories + fatCalories);
        double carbsG = Math.max(0.0, carbsCalories / 4.0);

        return new NutritionTargets(calories, proteinG, fatG, carbsG);
    }
}
