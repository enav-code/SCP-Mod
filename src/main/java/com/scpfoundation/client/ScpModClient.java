package com.scpfoundation.client;

import com.scpfoundation.ScpRegistry;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;

public class ScpModClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		EntityRendererRegistry.register(ScpRegistry.SCP_ENTITY, ScpEntityRenderer::new);
	}
}
