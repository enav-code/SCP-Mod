package com.scpfoundation;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.object.builder.v1.entity.FabricDefaultAttributeRegistry;
import net.minecraft.world.entity.monster.zombie.Zombie;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ScpMod implements ModInitializer {
	public static final String MOD_ID = "scpfoundation";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	@Override
	public void onInitialize() {
		ScpRegistry.init();
		FabricDefaultAttributeRegistry.register(ScpRegistry.SCP_ENTITY, Zombie.createAttributes());
		CommandRegistrationCallback.EVENT.register((dispatcher, ctx, env) -> ScpCommands.register(dispatcher));
		LOGGER.info("SCP Foundation loaded {} SCP entries", ScpRegistry.DEFINITIONS.size());
	}
}
