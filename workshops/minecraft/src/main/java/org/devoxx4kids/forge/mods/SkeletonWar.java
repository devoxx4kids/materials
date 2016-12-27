package org.devoxx4kids.forge.mods;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

import net.minecraft.entity.ai.EntityAINearestAttackableTarget;
import net.minecraft.entity.monster.EntityMob;
import net.minecraft.entity.monster.EntitySkeleton;
import net.minecraft.init.Items;
import net.minecraft.inventory.EntityEquipmentSlot;
import net.minecraft.item.ItemArmor;
import net.minecraft.item.ItemStack;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class SkeletonWar {

    @SubscribeEvent
    public void makeWarNotPeace(EntityJoinWorldEvent event) {
        if (!(event.getEntity() instanceof EntitySkeleton)) {
            return;
        }
        EntitySkeleton skeleton = (EntitySkeleton) event.getEntity();

        List<ItemArmor> helmets = Arrays.asList(Items.LEATHER_HELMET,
                Items.CHAINMAIL_HELMET, Items.GOLDEN_HELMET, Items.IRON_HELMET,
                Items.DIAMOND_HELMET);
        List<ItemArmor> chestplates = Arrays.asList(Items.LEATHER_CHESTPLATE,
                Items.CHAINMAIL_CHESTPLATE, Items.GOLDEN_CHESTPLATE,
                Items.IRON_CHESTPLATE, Items.DIAMOND_CHESTPLATE);
        List<ItemArmor> leggings = Arrays.asList(Items.LEATHER_LEGGINGS,
                Items.CHAINMAIL_LEGGINGS, Items.GOLDEN_LEGGINGS,
                Items.IRON_LEGGINGS, Items.DIAMOND_LEGGINGS);
        List<ItemArmor> boots = Arrays.asList(Items.LEATHER_BOOTS,
                Items.CHAINMAIL_BOOTS, Items.GOLDEN_BOOTS, Items.IRON_BOOTS,
                Items.DIAMOND_BOOTS);

        skeleton.targetTasks.addTask(3, new EntityAINearestAttackableTarget(
                skeleton, EntitySkeleton.class, true));
        skeleton.canPickUpLoot();

        Random random = new Random();
        skeleton.setItemStackToSlot(EntityEquipmentSlot.HEAD, new ItemStack(
                helmets.get(random.nextInt(5))));
        skeleton.setItemStackToSlot(EntityEquipmentSlot.CHEST, new ItemStack(
                chestplates.get(random.nextInt(5))));
        skeleton.setItemStackToSlot(EntityEquipmentSlot.LEGS, new ItemStack(
                leggings.get(random.nextInt(5))));
        skeleton.setItemStackToSlot(EntityEquipmentSlot.FEET,
                new ItemStack(boots.get(random.nextInt(5))));
    }

}
