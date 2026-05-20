package com.goalfuel;

import com.goalfuel.domain.NutritionTargets;
import com.goalfuel.domain.UserProfile;
import com.goalfuel.service.NutritionTargetsService;

public class Main {
    public static void main(String[] args) {
        UserProfile sample = new UserProfile("u1", 30, "male", 180, 80, "moderate", "muscle_gain", 3);
        NutritionTargetsService svc = new NutritionTargetsService();
        NutritionTargets t = svc.computeTargets(sample);
        System.out.println("Sample user targets:\n" + t);
    }
}
