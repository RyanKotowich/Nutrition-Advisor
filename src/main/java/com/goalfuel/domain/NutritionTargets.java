package com.goalfuel.domain;

public class NutritionTargets {
    private double caloriesTarget;
    private double proteinTargetG;
    private double fatTargetG;
    private double carbsTargetG;

    public NutritionTargets(double caloriesTarget, double proteinTargetG, double fatTargetG, double carbsTargetG) {
        this.caloriesTarget = caloriesTarget;
        this.proteinTargetG = proteinTargetG;
        this.fatTargetG = fatTargetG;
        this.carbsTargetG = carbsTargetG;
    }

    public double getCaloriesTarget() { return caloriesTarget; }
    public double getProteinTargetG() { return proteinTargetG; }
    public double getFatTargetG() { return fatTargetG; }
    public double getCarbsTargetG() { return carbsTargetG; }

    @Override
    public String toString() {
        return String.format("Calories: %.0f kcal, Protein: %.1fg, Fat: %.1fg, Carbs: %.1fg",
                caloriesTarget, proteinTargetG, fatTargetG, carbsTargetG);
    }
}
