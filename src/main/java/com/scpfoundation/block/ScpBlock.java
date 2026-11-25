package com.scpfoundation.block;

import com.scpfoundation.ScpDefinition;
import com.scpfoundation.behavior.BlockBehaviors;
import net.minecraft.core.BlockPos;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.BlockHitResult;

/** The block for a block-form SCP: stepping on it or right-clicking it runs its behaviors. */
public class ScpBlock extends Block {
	private final ScpDefinition def;

	public ScpBlock(Properties properties, ScpDefinition def) {
		super(properties);
		this.def = def;
	}

	@Override
	public void stepOn(Level level, BlockPos pos, BlockState state, Entity entity) {
		if (!level.isClientSide()) {
			for (String b : def.behaviors()) BlockBehaviors.onStep(b, level, pos, entity);
		}
		super.stepOn(level, pos, state, entity);
	}

	@Override
	protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
		if (level.isClientSide()) return InteractionResult.SUCCESS;
		boolean used = false;
		for (String b : def.behaviors()) used |= BlockBehaviors.onUse(b, level, pos, player);
		return used ? InteractionResult.SUCCESS : InteractionResult.PASS;
	}
}
