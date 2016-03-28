package org.devoxx4kids.forge.mods;

import net.minecraft.enchantment.Enchantment;
import net.minecraft.enchantment.EnchantmentHelper;
import net.minecraft.enchantment.EnumEnchantmentType;
import net.minecraft.init.Items;
import net.minecraft.inventory.EntityEquipmentSlot;
import net.minecraftforge.event.entity.living.LivingEntityUseItemEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class EnchantmentArrowFast extends Enchantment {
	public EnchantmentArrowFast(Enchantment.Rarity rarityIn, EntityEquipmentSlot... slots)
    {
        super(rarityIn, EnumEnchantmentType.BOW, slots);
        this.setName("arrowFast");
    }
    
	/**
	 * Returns the minimal value of enchantability needed on the enchantment
	 * level passed.
	 */
	public int getMinEnchantability(int enchantmentLevel) {
		return 12 + (enchantmentLevel - 1) * 20;
	}

	/**
	 * Returns the maximum value of enchantability nedded on the enchantment
	 * level passed.
	 */
	public int getMaxEnchantability(int enchantmentLevel) {
		return this.getMinEnchantability(enchantmentLevel) + 25;
	}

	/**
	 * Returns the maximum level that the enchantment can have.
	 */
	public int getMaxLevel() {
		return 2;
	}

	@SubscribeEvent
	public void decreaseBowUseDuration(LivingEntityUseItemEvent.Start event) {
		if (event.item == null) {
			return;
		}

		if (event.item.getItem() != Items.bow) {
			return;
		}

		int level = EnchantmentHelper.getEnchantmentLevel(MainMod.haste, event.item);

		switch (level) {
		case 2:
			event.duration -= 10;
			break;
		case 1:
			event.duration -= 5;
			break;
		default:
			break;
		}
	}
}