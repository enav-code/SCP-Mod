package com.scpfoundation;

import com.scpfoundation.block.KeycardDoorBlock;
import com.scpfoundation.block.ScpBlock;
import com.scpfoundation.entity.ScpEntity;
import com.scpfoundation.item.KeycardItem;
import com.scpfoundation.item.ScpArtifactItem;
import com.scpfoundation.item.TranquilizerGunItem;
import net.fabricmc.fabric.api.creativetab.v1.FabricCreativeModeTab;
import net.minecraft.core.Registry;
import net.minecraft.core.component.DataComponents;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.component.ItemLore;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.state.BlockBehaviour;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

public final class ScpRegistry {
	private ScpRegistry() {}

	public static final List<ScpDefinition> DEFINITIONS = ScpDefinition.loadAll();
	private static final Map<Integer, ScpDefinition> BY_NUMBER = new HashMap<>();
	public static final Map<Integer, Item> ITEM_BY_NUMBER = new HashMap<>();

	public static EntityType<ScpEntity> SCP_ENTITY;

	private static final List<ItemStack> TAB_FOUNDATION = new ArrayList<>();
	private static final Map<String, List<ItemStack>> TAB_BY_CLASS = new HashMap<>();
	private static Item tabIconFoundation;

	public static ScpDefinition byNumber(int n) { return BY_NUMBER.get(n); }

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(ScpMod.MOD_ID, path);
	}

	public static void init() {
		registerEntity();
		for (ScpDefinition def : DEFINITIONS) {
			BY_NUMBER.put(def.n(), def);
			registerScp(def);
		}
		registerFacility();
		registerTabs();
	}

	private static void registerEntity() {
		ResourceKey<EntityType<?>> key = ResourceKey.create(Registries.ENTITY_TYPE, id("scp_entity"));
		SCP_ENTITY = Registry.register(BuiltInRegistries.ENTITY_TYPE, key,
				EntityType.Builder.<ScpEntity>of(ScpEntity::new, MobCategory.MONSTER).sized(0.6F, 1.95F).build(key));
	}

	private static ItemLore lore(ScpDefinition def) {
		List<Component> lines = new ArrayList<>();
		lines.add(Component.literal("Object Class: " + def.cls()));
		lines.add(Component.literal("Form: " + def.form()));
		lines.add(Component.literal("Anomalous properties: " + String.join(", ", def.behaviors())));
		if (!def.canon()) lines.add(Component.literal("(class and behaviors are generated: edit tools/scp_overrides.psv)"));
		return new ItemLore(lines);
	}

	private static void registerScp(ScpDefinition def) {
		Item item;
		if (def.isBlock()) {
			ResourceKey<Block> bk = ResourceKey.create(Registries.BLOCK, id(def.id()));
			Block block = Registry.register(BuiltInRegistries.BLOCK, bk,
					new ScpBlock(BlockBehaviour.Properties.of().strength(4.0F, 12.0F).setId(bk), def));
			ResourceKey<Item> ik = ResourceKey.create(Registries.ITEM, id(def.id()));
			item = Registry.register(BuiltInRegistries.ITEM, ik, new BlockItem(block,
					new Item.Properties().setId(ik).useBlockDescriptionPrefix().component(DataComponents.LORE, lore(def))));
		} else {
			ResourceKey<Item> ik = ResourceKey.create(Registries.ITEM, id(def.id()));
			item = Registry.register(BuiltInRegistries.ITEM, ik, new ScpArtifactItem(
					new Item.Properties().setId(ik).stacksTo(def.isEntity() ? 16 : 1).component(DataComponents.LORE, lore(def)), def));
		}
		ITEM_BY_NUMBER.put(def.n(), item);
		String tab = switch (def.cls()) {
			case "Safe" -> "safe";
			case "Euclid" -> "euclid";
			case "Keter" -> "keter";
			default -> "other";
		};
		TAB_BY_CLASS.computeIfAbsent(tab, k -> new ArrayList<>()).add(new ItemStack(item));
	}

	private static Block facilityBlock(String name, Function<BlockBehaviour.Properties, Block> factory, float hardness) {
		ResourceKey<Block> bk = ResourceKey.create(Registries.BLOCK, id(name));
		Block block = Registry.register(BuiltInRegistries.BLOCK, bk,
				factory.apply(BlockBehaviour.Properties.of().strength(hardness, 1200.0F).requiresCorrectToolForDrops().setId(bk)));
		ResourceKey<Item> ik = ResourceKey.create(Registries.ITEM, id(name));
		Item bi = Registry.register(BuiltInRegistries.ITEM, ik,
				new BlockItem(block, new Item.Properties().setId(ik).useBlockDescriptionPrefix()));
		TAB_FOUNDATION.add(new ItemStack(bi));
		if (tabIconFoundation == null) tabIconFoundation = bi;
		return block;
	}

	private static void registerFacility() {
		facilityBlock("containment_wall", Block::new, 50.0F);
		facilityBlock("reinforced_floor", Block::new, 50.0F);
		facilityBlock("hazard_stripe", Block::new, 5.0F);
		facilityBlock("containment_lamp", p -> new Block(p.lightLevel(s -> 15)), 5.0F);
		facilityBlock("foundation_logo", Block::new, 5.0F);
		for (int lvl = 0; lvl <= 5; lvl++) {
			final int level = lvl;
			facilityBlock("keycard_door_" + lvl, p -> new KeycardDoorBlock(p.noOcclusion(), level), 50.0F);
		}
		for (int lvl = 0; lvl <= 5; lvl++) {
			final int level = lvl;
			ResourceKey<Item> ik = ResourceKey.create(Registries.ITEM, id("keycard_" + lvl));
			Item card = Registry.register(BuiltInRegistries.ITEM, ik,
					new KeycardItem(new Item.Properties().setId(ik).stacksTo(1), level));
			TAB_FOUNDATION.add(new ItemStack(card));
		}
		ResourceKey<Item> gk = ResourceKey.create(Registries.ITEM, id("tranquilizer_gun"));
		Item gun = Registry.register(BuiltInRegistries.ITEM, gk,
				new TranquilizerGunItem(new Item.Properties().setId(gk).stacksTo(1)));
		TAB_FOUNDATION.add(new ItemStack(gun));
	}

	private static void registerTabs() {
		tab("foundation", TAB_FOUNDATION);
		for (String t : new String[]{"safe", "euclid", "keter", "other"}) {
			tab(t, TAB_BY_CLASS.getOrDefault(t, List.of()));
		}
	}

	private static void tab(String name, List<ItemStack> stacks) {
		ItemStack icon = stacks.isEmpty() ? new ItemStack(net.minecraft.world.item.Items.PAPER) : stacks.get(0);
		CreativeModeTab tab = FabricCreativeModeTab.builder()
				.title(Component.translatable("itemGroup." + ScpMod.MOD_ID + "." + name))
				.icon(() -> icon)
				.displayItems((params, output) -> stacks.forEach(output::accept))
				.build();
		Registry.register(BuiltInRegistries.CREATIVE_MODE_TAB, id(name), tab);
	}
}
