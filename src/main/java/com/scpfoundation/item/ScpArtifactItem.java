package com.scpfoundation.item;

import com.scpfoundation.ScpDefinition;
import com.scpfoundation.ScpRegistry;
import com.scpfoundation.behavior.ItemBehaviors;
import com.scpfoundation.entity.ScpEntity;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.level.Level;

/**
 * The item for an item-form or entity-form SCP.
 * Item form: right-click applies its behaviors. Entity form: right-click on a block spawns the SCP.
 */
public class ScpArtifactItem extends Item {
	private final ScpDefinition def;

	public ScpArtifactItem(Properties properties, ScpDefinition def) {
		super(properties);
		this.def = def;
	}

	@Override
	public InteractionResult use(Level level, Player player, InteractionHand hand) {
		if (!def.isItem()) return InteractionResult.PASS;
		if (!level.isClientSide()) {
			for (String b : def.behaviors()) ItemBehaviors.apply(b, player);
			player.getCooldowns().addCooldown(player.getItemInHand(hand), 200);
		}
		return InteractionResult.SUCCESS;
	}

	@Override
	public InteractionResult useOn(UseOnContext ctx) {
		if (!def.isEntity()) return InteractionResult.PASS;
		Level level = ctx.getLevel();
		if (level.isClientSide()) return InteractionResult.SUCCESS;
		BlockPos pos = ctx.getClickedPos().relative(ctx.getClickedFace() == Direction.DOWN ? Direction.DOWN : Direction.UP);
		ScpEntity e = ScpRegistry.SCP_ENTITY.create(level, EntitySpawnReason.SPAWN_ITEM_USE);
		if (e == null) return InteractionResult.FAIL;
		e.setPos(pos.getX() + 0.5, pos.getY(), pos.getZ() + 0.5);
		e.setScp(def);
		level.addFreshEntity(e);
		if (ctx.getPlayer() != null && !ctx.getPlayer().isCreative()) ctx.getItemInHand().shrink(1);
		return InteractionResult.SUCCESS;
	}
}
