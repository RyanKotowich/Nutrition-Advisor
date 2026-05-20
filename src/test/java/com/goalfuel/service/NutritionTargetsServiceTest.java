package com.goalfuel.service;

import com.goalfuel.domain.NutritionTargets;
import com.goalfuel.domain.UserProfile;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class NutritionTargetsServiceTest {

    @Test
    public void computesReasonableTargets() {
        UserProfile u = new UserProfile("t1", 40, "female", 165, 70, "light", "weight_loss", 3);
        NutritionTargetsService svc = new NutritionTargetsService();
        NutritionTargets t = svc.computeTargets(u);
        assertTrue(t.getCaloriesTarget() > 1100 && t.getCaloriesTarget() < 2200);
        assertTrue(t.getProteinTargetG() > 60 && t.getProteinTargetG() < 140);
        assertTrue(t.getFatTargetG() > 25 && t.getFatTargetG() < 100);
        assertTrue(t.getCarbsTargetG() > 50);
    }
}
