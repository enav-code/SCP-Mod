package com.scpfoundation.behavior;

import net.minecraft.core.Holder;
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.Vec3;

/** Small shared helpers used by entity, item and block behaviors. */
public final class Effects {
	private Effects() {}

	public static void give(LivingEntity e, Holder<MobEffect> effect, int ticks, int amp) {
		e.addEffect(new MobEffectInstance(effect, ticks, amp));
	}

	public static boolean targetable(Player p) {
		return !p.isCreative() && !p.isSpectator();
	}

	/** True when the player's crosshair is roughly on the entity and nothing blocks the view. */
	public static boolean isLookedAt(Player p, LivingEntity e) {
		Vec3 look = p.getViewVector(1.0F).normalize();
		Vec3 to = e.getEyePosition().subtract(p.getEyePosition()).normalize();
		return look.dot(to) > 0.96 && p.hasLineOfSight(e);
	}

	public static final Holder<MobEffect> SLOWNESS = MobEffects.SLOWNESS;
}
