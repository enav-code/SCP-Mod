package com.scpfoundation.item;

import net.minecraft.world.item.Item;

/** Keycards, level 0 to 5. A door opens when the holder carries a card of equal or higher level. */
public class KeycardItem extends Item {
	private final int level;

	public KeycardItem(Properties properties, int level) {
		super(properties);
		this.level = level;
	}

	public int level() { return level; }
}
