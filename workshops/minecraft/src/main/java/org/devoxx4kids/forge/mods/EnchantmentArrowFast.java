package org.devoxx4kids.forge.mods;

import net.minecraft.enchantment.Enchantment;
import net.minecraft.enchantment.EnchantmentHelper;
import net.minecraft.enchantment.EnumEnchantmentType;
import net.minecraft.init.Items;
import net.minecraft.inventory.EntityEquipmentSlot;
import net.minecraftforge.event.entity.living.LivingEntityUseItemEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class EnchantmentArrowFast extends Enchantment {

    public EnchantmentArrowFast() {
        super(Enchantment.Rarity.UNCOMMON, EnumEnchantmentType.BOW,
                new EntityEquipmentSlot[]{EntityEquipmentSlot.MAINHAND,
                    EntityEquipmentSlot.OFFHAND});
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
    public void decreaseBowUseDuration(LivingEntityUseItemEvent.Tick event) {
        if (event.getItem() == null) {
            return;
        }

        if (event.getItem().getItem() != Items.BOW) {
            return;
        }

        int level = EnchantmentHelper.getEnchantmentLevel(MainMod.haste, event.getItem());

        switch (level) {
            case 1:
                event.setDuration(event.getDuration() - 1);
                break;
            case 2:
                event.setDuration(event.getDuration() - 2);
                break;
            default:
                break;
        }
    }
}
