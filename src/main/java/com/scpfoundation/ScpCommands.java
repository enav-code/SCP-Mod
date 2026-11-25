package com.scpfoundation;

import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.scpfoundation.entity.ScpEntity;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;

import java.util.List;

/**
 * /scp give <0-2000>   give yourself that SCP
 * /scp info <0-2000>   show class, form and behaviors
 * /breach [count]      containment breach: spawns random Euclid/Keter SCP entities around you
 */
public final class ScpCommands {
	private ScpCommands() {}

	public static void register(CommandDispatcher<CommandSourceStack> d) {
		d.register(Commands.literal("scp").requires(Commands.hasPermission(Commands.LEVEL_GAMEMASTERS))
				.then(Commands.literal("give").then(Commands.argument("number", IntegerArgumentType.integer(0, 2000))
						.executes(c -> give(c.getSource(), IntegerArgumentType.getInteger(c, "number")))))
				.then(Commands.literal("info").then(Commands.argument("number", IntegerArgumentType.integer(0, 2000))
						.executes(c -> info(c.getSource(), IntegerArgumentType.getInteger(c, "number")))))
				.then(Commands.literal("recipe").then(Commands.argument("number", IntegerArgumentType.integer(0, 2000))
						.executes(c -> recipe(c.getSource(), IntegerArgumentType.getInteger(c, "number"))))));
		d.register(Commands.literal("breach").requires(Commands.hasPermission(Commands.LEVEL_GAMEMASTERS))
				.executes(c -> breach(c.getSource(), 5))
				.then(Commands.argument("count", IntegerArgumentType.integer(1, 30))
						.executes(c -> breach(c.getSource(), IntegerArgumentType.getInteger(c, "count")))));
	}

	private static int give(CommandSourceStack src, int n) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
		ServerPlayer p = src.getPlayerOrException();
		Item item = ScpRegistry.ITEM_BY_NUMBER.get(n);
		p.getInventory().add(new ItemStack(item));
		src.sendSuccess(() -> Component.literal("Gave " + ScpRegistry.byNumber(n).title()), false);
		return 1;
	}

	private static int recipe(CommandSourceStack src, int n) {
		ScpDefinition d = ScpRegistry.byNumber(n);
		src.sendSuccess(() -> Component.literal(d.title() + " crafts shapeless from: "
				+ String.join(", ", d.recipe().stream().map(s -> s.replace("minecraft:", "")).toList())), false);
		return 1;
	}

	private static int info(CommandSourceStack src, int n) {
		ScpDefinition d = ScpRegistry.byNumber(n);
		src.sendSuccess(() -> Component.literal(d.title() + " | Class: " + d.cls() + " | Form: " + d.form()
				+ (d.isEntity() ? " | Size: x" + d.scale() + " (" + d.sizeSrc() + ")" : "")
				+ " | Behaviors: " + String.join(", ", d.behaviors()) + (d.canon() ? "" : " | (generated stand-in)")), false);
		return 1;
	}

	private static int breach(CommandSourceStack src, int count) throws com.mojang.brigadier.exceptions.CommandSyntaxException {
		ServerPlayer p = src.getPlayerOrException();
		ServerLevel level = p.level();
		List<ScpDefinition> pool = ScpRegistry.DEFINITIONS.stream()
				.filter(d -> d.isEntity() && (d.cls().equals("Euclid") || d.cls().equals("Keter"))
						&& !d.behaviors().contains("PASSIVE")).toList();
		int spawned = 0;
		for (int i = 0; i < count; i++) {
			ScpDefinition d = pool.get(level.getRandom().nextInt(pool.size()));
			ScpEntity e = ScpRegistry.SCP_ENTITY.create(level, EntitySpawnReason.COMMAND);
			if (e == null) continue;
			double ang = level.getRandom().nextDouble() * Math.PI * 2;
			double r = 8 + level.getRandom().nextDouble() * 8;
			e.setPos(p.getX() + Math.cos(ang) * r, p.getY(), p.getZ() + Math.sin(ang) * r);
			e.setScp(d);
			level.addFreshEntity(e);
			spawned++;
		}
		final int n = spawned;
		src.sendSuccess(() -> Component.literal("CONTAINMENT BREACH: " + n + " SCP entities loose."), true);
		return spawned;
	}
}
