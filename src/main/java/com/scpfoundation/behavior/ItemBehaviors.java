package com.scpfoundation.behavior;

import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

import java.util.List;

/** Effects of SCP "item" form artifacts when right-clicked. */
public final class ItemBehaviors {
	private ItemBehaviors() {}

	public static void apply(String behavior, Player p) {
		switch (behavior) {
			case "HEAL" -> p.heal(10.0F);
			case "SPEED_BURST" -> Effects.give(p, MobEffects.SPEED, 600, 2);
			case "NIGHT_VISION" -> Effects.give(p, MobEffects.NIGHT_VISION, 3600, 0);
			case "LEVITATE_SELF" -> {
				Effects.give(p, MobEffects.LEVITATION, 50, 0);
				Effects.give(p, MobEffects.SLOW_FALLING, 400, 0);
			}
			case "BLINK" -> blink(p);
			case "REGENERATION" -> Effects.give(p, MobEffects.REGENERATION, 300, 1);
			case "FIRE_PROOF" -> Effects.give(p, MobEffects.FIRE_RESISTANCE, 3600, 0);
			case "STRENGTH" -> Effects.give(p, MobEffects.STRENGTH, 600, 1);
			case "FEED" -> p.getFoodData().eat(8, 1.0F);
			case "REPEL" -> repel(p);
			case "ABSORB_COST" -> {
				Effects.give(p, MobEffects.ABSORPTION, 1200, 3);
				Effects.give(p, MobEffects.HUNGER, 400, 2);
			}
			case "RESIST" -> Effects.give(p, MobEffects.RESISTANCE, 600, 1);
			default -> { }
		}
	}

	private static void blink(Player p) {
		HitResult hit = p.pick(10.0, 1.0F, false);
		Vec3 look = p.getViewVector(1.0F);
		Vec3 target = hit.getLocation().subtract(look.scale(0.6));
		if (p instanceof ServerPlayer sp) {
			sp.connection.teleport(target.x, target.y, target.z, sp.getYRot(), sp.getXRot());
		}
	}

	private static void repel(Player p) {
		List<LivingEntity> near = p.level().getEntitiesOfClass(LivingEntity.class,
				p.getBoundingBox().inflate(6.0), e -> e != p);
		for (LivingEntity e : near) {
			Vec3 away = e.position().subtract(p.position()).normalize().scale(1.4).add(0, 0.4, 0);
			e.setDeltaMovement(away);
		}
	}
}
