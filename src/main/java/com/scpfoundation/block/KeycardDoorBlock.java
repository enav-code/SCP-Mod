package com.scpfoundation.block;

import com.scpfoundation.item.KeycardItem;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.util.RandomSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.BlockGetter;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.level.block.state.StateDefinition;
import net.minecraft.world.level.block.state.properties.BlockStateProperties;
import net.minecraft.world.level.block.state.properties.BooleanProperty;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.shapes.CollisionContext;
import net.minecraft.world.phys.shapes.Shapes;
import net.minecraft.world.phys.shapes.VoxelShape;

/** A solid block that becomes walk-through for 3 seconds when right-clicked with a high enough keycard. */
public class KeycardDoorBlock extends Block {
	public static final BooleanProperty OPEN = BlockStateProperties.OPEN;
	private final int requiredLevel;

	public KeycardDoorBlock(Properties properties, int requiredLevel) {
		super(properties);
		this.requiredLevel = requiredLevel;
		registerDefaultState(stateDefinition.any().setValue(OPEN, false));
	}

	@Override
	protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
		builder.add(OPEN);
	}

	@Override
	protected VoxelShape getCollisionShape(BlockState state, BlockGetter level, BlockPos pos, CollisionContext ctx) {
		return state.getValue(OPEN) ? Shapes.empty() : Shapes.block();
	}

	@Override
	protected InteractionResult useWithoutItem(BlockState state, Level level, BlockPos pos, Player player, BlockHitResult hit) {
		if (level.isClientSide()) return InteractionResult.SUCCESS;
		if (state.getValue(OPEN)) return InteractionResult.SUCCESS;
		if (hasKeycard(player)) {
			level.setBlock(pos, state.setValue(OPEN, true), Block.UPDATE_ALL);
			level.scheduleTick(pos, this, 60);
		} else {
			player.sendOverlayMessage(Component.literal("Access denied: Level " + requiredLevel + " keycard required."));
		}
		return InteractionResult.SUCCESS;
	}

	private boolean hasKeycard(Player p) {
		if (p.isCreative()) return true;
		for (ItemStack s : new ItemStack[]{p.getMainHandItem(), p.getOffhandItem()}) {
			if (s.getItem() instanceof KeycardItem k && k.level() >= requiredLevel) return true;
		}
		return false;
	}

	@Override
	protected void tick(BlockState state, ServerLevel level, BlockPos pos, RandomSource random) {
		if (state.getValue(OPEN)) level.setBlock(pos, state.setValue(OPEN, false), Block.UPDATE_ALL);
	}
}
