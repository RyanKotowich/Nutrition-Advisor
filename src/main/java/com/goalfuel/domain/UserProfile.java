package com.goalfuel.domain;

public class UserProfile {
    private final String id;
    private final int age;
    private final String sex; // "male" or "female"
    private final double heightCm;
    private final double weightKg;
    private final String activityLevel; // sedentary, light, moderate, active, very_active
    private final String goal; // weight_loss, muscle_gain, maintain
    private final int mealsPerDay;

    public UserProfile(String id, int age, String sex, double heightCm, double weightKg, String activityLevel, String goal, int mealsPerDay) {
        this.id = id;
        this.age = age;
        this.sex = sex;
        this.heightCm = heightCm;
        this.weightKg = weightKg;
        this.activityLevel = activityLevel;
        this.goal = goal;
        this.mealsPerDay = mealsPerDay;
    }

    public String getId() { return id; }
    public int getAge() { return age; }
    public String getSex() { return sex; }
    public double getHeightCm() { return heightCm; }
    public double getWeightKg() { return weightKg; }
    public String getActivityLevel() { return activityLevel; }
    public String getGoal() { return goal; }
    public int getMealsPerDay() { return mealsPerDay; }
}
