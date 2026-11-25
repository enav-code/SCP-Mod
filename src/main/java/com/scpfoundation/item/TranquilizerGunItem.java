package com.scpfoundation.item;

import com.scpfoundation.behavior.Effects;
import com.scpfoundation.entity.ScpEntity;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

import java.util.List;

/** Instant-hit sedative: freezes SCP entities for 15 s, slows and weakens anything else. */
public class TranquilizerGunItem extends Item {
	public TranquilizerGunItem(Properties properties) {
		super(properties);
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		if (level.isClientSide()) return InteractionResult.SUCCESS;
		Vec3 look = player.getViewVector(1.0F).normalize();
		Vec3 eye = player.getEyePosition();
		List<LivingEntity> candidates = level.getEntitiesOfClass(LivingEntity.class,
				player.getBoundingBox().expandTowards(look.scale(24.0)).inflate(1.0), e -> e != player);
		LivingEntity best = null;
		double bestDot = 0.985;
		for (LivingEntity e : candidates) {
			Vec3 to = e.getEyePosition().subtract(eye).normalize();
			double dot = look.dot(to);
			if (dot > bestDot && player.hasLineOfSight(e) && e.distanceTo(player) <= 24.0) {
				best = e;
				bestDot = dot;
			}
		}
		if (best != null) {
			if (best instanceof ScpEntity scp) scp.sedate(300);
			Effects.give(best, MobEffects.SLOWNESS, 300, 4);
			Effects.give(best, MobEffects.WEAKNESS, 300, 2);
		}
		player.getCooldowns().addCooldown(player.getItemInHand(hand), 40);
		return InteractionResult.SUCCESS;
	}
}
