package com.scpfoundation.behavior;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.item.ItemEntity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ItemLike;
import net.minecraft.world.level.Level;

import java.util.List;

/** Effects of SCP "block" form anomalies when stepped on or right-clicked. */
public final class BlockBehaviors {
	private BlockBehaviors() {}

	private static final List<ItemLike> LOOT = List.of(
			Items.GOLDEN_APPLE, Items.DIAMOND, Items.ENDER_PEARL, Items.COOKED_BEEF, Items.EMERALD,
			Items.IRON_INGOT, Items.GOLD_INGOT, Items.REDSTONE, Items.LAPIS_LAZULI, Items.COOKIE);

	public static void onStep(String behavior, Level level, BlockPos pos, Entity entity) {
		if (!(entity instanceof LivingEntity living)) return;
		switch (behavior) {
			case "LAUNCH_PAD" -> {
				living.setDeltaMovement(living.getDeltaMovement().x, 1.2, living.getDeltaMovement().z);
			}
			case "HARM_ON_STEP" -> Effects.give(living, MobEffects.POISON, 60, 0);
			case "SLOW_ON_STEP" -> Effects.give(living, MobEffects.SLOWNESS, 60, 2);
			default -> { }
		}
	}

	/** @return true when the behavior consumed the interaction. */
	public static boolean onUse(String behavior, Level level, BlockPos pos, Player p) {
		switch (behavior) {
			case "HEAL_ON_USE" -> {
				p.heal(6.0F);
				return true;
			}
			case "USE_EFFECT" -> {
				switch (level.getRandom().nextInt(4)) {
					case 0 -> Effects.give(p, MobEffects.SPEED, 400, 1);
					case 1 -> Effects.give(p, MobEffects.JUMP_BOOST, 400, 1);
					case 2 -> Effects.give(p, MobEffects.REGENERATION, 200, 1);
					default -> Effects.give(p, MobEffects.NIGHT_VISION, 1200, 0);
				}
				return true;
			}
			case "USE_TELEPORT" -> {
				if (p instanceof ServerPlayer sp) {
					double dx = (level.getRandom().nextDouble() - 0.5) * 40;
					double dz = (level.getRandom().nextDouble() - 0.5) * 40;
					sp.connection.teleport(pos.getX() + dx, pos.getY() + 2, pos.getZ() + dz, sp.getYRot(), sp.getXRot());
				}
				return true;
			}
			case "USE_LOOT" -> {
				ItemLike item = LOOT.get(level.getRandom().nextInt(LOOT.size()));
				level.addFreshEntity(new ItemEntity(level, pos.getX() + 0.5, pos.getY() + 1.1, pos.getZ() + 0.5, new ItemStack(item)));
				return true;
			}
			default -> {
				return false;
			}
		}
	}
}
