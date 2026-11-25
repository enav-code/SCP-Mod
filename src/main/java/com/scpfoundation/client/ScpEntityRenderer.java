package com.scpfoundation.client;

import com.scpfoundation.ScpRegistry;
import com.scpfoundation.entity.ScpEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.ZombieRenderer;
import net.minecraft.client.renderer.entity.state.ZombieRenderState;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.monster.zombie.Zombie;

/** Vanilla humanoid model, with a different skin per SCP (textures/entity/scp/scp_NNNN.png) and per-SCP scale. */
public class ScpEntityRenderer extends ZombieRenderer {
	public static class State extends ZombieRenderState {
		public int scp = -1;
	}

	public ScpEntityRenderer(EntityRendererProvider.Context ctx) {
		super(ctx);
	}

	@Override
	public ZombieRenderState createRenderState() {
		return new State();
	}

	@Override
	public void extractRenderState(Zombie entity, ZombieRenderState state, float partialTick) {
		super.extractRenderState(entity, state, partialTick);
		if (state instanceof State s && entity instanceof ScpEntity e) s.scp = e.scpNumber();
	}

	@Override
	public Identifier getTextureLocation(ZombieRenderState state) {
		int n = state instanceof State s ? s.scp : -1;
		if (n < 0) return ScpRegistry.id("textures/entity/scp_entity.png");
		return ScpRegistry.id(String.format("textures/entity/scp/scp_%04d.png", n));
	}
}
