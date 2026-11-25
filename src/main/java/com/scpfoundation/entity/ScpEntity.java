package com.scpfoundation.entity;

import com.scpfoundation.ScpDefinition;
import com.scpfoundation.ScpRegistry;
import com.scpfoundation.behavior.Effects;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EntityTypes;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.monster.zombie.Zombie;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import net.minecraft.world.phys.Vec3;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * One generic entity type that becomes any of the ~700 entity-form SCPs. The SCP number is stored in NBT,
 * stats come from the SCP's class, and every behavior in its definition runs from {@link #tick()}.
 * Extends Zombie only so the vanilla humanoid renderer can be reused.
 */
public class ScpEntity extends Zombie {
	private static final EntityDataAccessor<Integer> DATA_SCP = SynchedEntityData.defineId(ScpEntity.class, EntityDataSerializers.INT);
	private int scpNumber = -1;
	private Set<String> behaviors = new HashSet<>();
	private int sedatedTicks = 0;

	public ScpEntity(EntityType<? extends Zombie> type, Level level) {
		super(type, level);
	}

	@Override
	protected void defineSynchedData(SynchedEntityData.Builder builder) {
		super.defineSynchedData(builder);
		builder.define(DATA_SCP, -1);
	}

	/** SCP number for the client renderer (picks the per-SCP skin). */
	public int scpNumber() { return entityData.get(DATA_SCP); }

	public void setScp(ScpDefinition def) {
		this.scpNumber = def.n();
		entityData.set(DATA_SCP, def.n());
		getAttribute(Attributes.SCALE).setBaseValue(def.scale());
		this.behaviors = new HashSet<>(def.behaviors());
		getAttribute(Attributes.MAX_HEALTH).setBaseValue(def.hp());
		getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(def.dmg());
		double speed = 0.23 * (behaviors.contains("FAST") ? 1.8 : 1.0);
		getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(speed);
		setHealth(def.hp());
		setCustomName(Component.literal(def.title()));
		setCustomNameVisible(true);
		setPersistenceRequired();
	}

	public void sedate(int ticks) { this.sedatedTicks = Math.max(sedatedTicks, ticks); }

	private boolean has(String b) { return behaviors.contains(b); }

	// ---- vanilla zombie behavior we do not want ----
	@Override protected boolean isSunSensitive() { return false; }
	@Override protected boolean convertsInWater() { return false; }
	@Override public boolean fireImmune() { return has("FIRE_AURA") || super.fireImmune(); }

	@Override
	protected void registerGoals() {
		goalSelector.addGoal(0, new FloatGoal(this));
		goalSelector.addGoal(2, new MeleeAttackGoal(this, 1.0, false));
		goalSelector.addGoal(7, new WaterAvoidingRandomStrollGoal(this, 0.8));
		goalSelector.addGoal(8, new LookAtPlayerGoal(this, Player.class, 8.0F));
		goalSelector.addGoal(8, new RandomLookAroundGoal(this));
		targetSelector.addGoal(1, new HurtByTargetGoal(this));
		targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
	}

	// ---- per-tick behavior ----
	@Override
	public void tick() {
		if (level() instanceof ServerLevel sl) serverBehavior(sl);
		super.tick();
	}

	private void serverBehavior(ServerLevel sl) {
		if (has("PASSIVE") && getTarget() != null) setTarget(null);

		List<Player> players = sl.getEntitiesOfClass(Player.class, getBoundingBox().inflate(16.0),
				Effects::targetable);
		boolean watched = false;
		Player watcher = null;
		for (Player p : players) {
			if (Effects.isLookedAt(p, this)) { watched = true; watcher = p; break; }
		}

		// freeze: sedated by tranquilizer, or frozen while observed (SCP-173 style)
		if (sedatedTicks > 0) sedatedTicks--;
		setNoAi(sedatedTicks > 0 || (has("WATCHED_FREEZE") && watched));

		if (has("RAGE_WHEN_LOOKED") && watched && watcher != null) {
			setTarget(watcher);
			Effects.give(this, MobEffects.SPEED, 100, 2);
			Effects.give(this, MobEffects.STRENGTH, 100, 2);
		}

		int t = tickCount;
		if (t % 20 == 0) {
			if (has("REGEN")) heal(1.0F);
			for (Player p : players) {
				double d = distanceTo(p);
				if (has("HEAL_AURA") && d < 8) Effects.give(p, MobEffects.REGENERATION, 60, 0);
				if (has("FIRE_AURA") && d < 4) p.setRemainingFireTicks(80);
				if (has("DARKNESS_AURA") && d < 10) Effects.give(p, MobEffects.DARKNESS, 100, 0);
				if (has("WITHER_AURA") && d < 5) Effects.give(p, MobEffects.WITHER, 60, 0);
				if (has("SLOW_FIELD") && d < 6) Effects.give(p, MobEffects.SLOWNESS, 60, 1);
				if (has("BLIND_STARE") && d < 24 && Effects.isLookedAt(p, this)) Effects.give(p, MobEffects.BLINDNESS, 80, 0);
			}
		}
		if (has("PULL_PLAYERS") && t % 2 == 0) {
			for (Player p : players) {
				double d = distanceTo(p);
				if (d < 10 && d > 1.5) {
					Vec3 dir = position().subtract(p.position()).normalize().scale(0.08);
					p.setDeltaMovement(p.getDeltaMovement().add(dir));
				}
			}
		}
		LivingEntity target = getTarget();
		if (target != null && !isNoAi()) {
			double d = distanceTo(target);
			if (has("TELEPORT_STRIKE") && t % 40 == 0 && d > 4 && d < 24
					&& !(target instanceof Player tp && Effects.isLookedAt(tp, this))) {
				Vec3 look = target.getViewVector(1.0F).multiply(1, 0, 1).normalize();
				setPos(target.getX() - look.x * 1.5, target.getY(), target.getZ() - look.z * 1.5);
				getNavigation().stop();
			}
			if (has("SUMMON_MINIONS") && t % 200 == 0 && d < 20) {
				for (int i = 0; i < 2; i++) {
					Zombie z = EntityTypes.ZOMBIE.create(sl, EntitySpawnReason.MOB_SUMMONED);
					if (z != null) {
						z.setPos(getX() + random.nextInt(5) - 2, getY(), getZ() + random.nextInt(5) - 2);
						z.setTarget(target);
						sl.addFreshEntity(z);
					}
				}
			}
		}
		if (has("BLINK") && t % 100 == 0 && !isNoAi()) {
			setPos(getX() + random.nextInt(17) - 8, getY(), getZ() + random.nextInt(17) - 8);
		}
	}

	// ---- on-hit effects ----
	@Override
	public boolean doHurtTarget(ServerLevel level, Entity target) {
		boolean hit = super.doHurtTarget(level, target);
		if (hit && target instanceof LivingEntity le) {
			if (has("POISON_TOUCH")) Effects.give(le, MobEffects.POISON, 120, 1);
			if (has("WEAKEN_TOUCH")) Effects.give(le, MobEffects.WEAKNESS, 200, 1);
			if (has("LEVITATE_TOUCH")) Effects.give(le, MobEffects.LEVITATION, 40, 0);
		}
		return hit;
	}

	@Override
	public boolean hurtServer(ServerLevel level, DamageSource source, float amount) {
		boolean hurt = super.hurtServer(level, source, amount);
		if (hurt && has("THORNS") && source.getEntity() instanceof LivingEntity attacker && attacker != this) {
			attacker.hurtServer(level, level.damageSources().thorns(this), 2.0F);
		}
		return hurt;
	}

	@Override
	public void die(DamageSource source) {
		if (has("EXPLODE_ON_DEATH") && level() instanceof ServerLevel sl) {
			sl.explode(this, getX(), getY(), getZ(), 2.5F, Level.ExplosionInteraction.NONE);
		}
		super.die(source);
	}

	// ---- persistence ----
	@Override
	protected void addAdditionalSaveData(ValueOutput output) {
		super.addAdditionalSaveData(output);
		output.putInt("Scp", scpNumber);
	}

	@Override
	protected void readAdditionalSaveData(ValueInput input) {
		super.readAdditionalSaveData(input);
		int n = input.getIntOr("Scp", -1);
		if (n >= 0) {
			ScpDefinition def = ScpRegistry.byNumber(n);
			if (def != null) setScp(def);
		}
	}
}
