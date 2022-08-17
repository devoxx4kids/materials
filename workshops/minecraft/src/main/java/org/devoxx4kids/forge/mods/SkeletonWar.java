package org.devoxx4kids.forge.mods;

import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.AbstractSkeleton;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

import java.util.Arrays;
import java.util.List;

@Mod.EventBusSubscriber(modid = MainMod.MODID)
public class SkeletonWar {
    static List<Item> helmets = Arrays.asList(Items.LEATHER_HELMET,
            Items.CHAINMAIL_HELMET, Items.GOLDEN_HELMET, Items.IRON_HELMET,
            Items.DIAMOND_HELMET, Items.NETHERITE_HELMET, Items.TURTLE_HELMET);
    static List<Item> chestplates = Arrays.asList(Items.LEATHER_CHESTPLATE,
            Items.CHAINMAIL_CHESTPLATE, Items.GOLDEN_CHESTPLATE, Items.IRON_CHESTPLATE,
            Items.DIAMOND_CHESTPLATE, Items.NETHERITE_CHESTPLATE);
    static List<Item> leggings = Arrays.asList(Items.LEATHER_LEGGINGS,
            Items.CHAINMAIL_LEGGINGS, Items.GOLDEN_LEGGINGS, Items.IRON_LEGGINGS,
            Items.DIAMOND_LEGGINGS, Items.NETHERITE_LEGGINGS);
    static List<Item> boots = Arrays.asList(Items.LEATHER_BOOTS,
            Items.CHAINMAIL_BOOTS, Items.GOLDEN_BOOTS, Items.IRON_BOOTS,
            Items.DIAMOND_BOOTS, Items.NETHERITE_BOOTS);

    @SubscribeEvent
    public static void makeWarNotPeace(EntityJoinLevelEvent event) {
        if (!(event.getEntity() instanceof AbstractSkeleton skeleton)) {
            return;
        }

        skeleton.targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(skeleton, AbstractSkeleton.class, true));

        RandomSource random = skeleton.level.random;
        skeleton.setItemSlot(EquipmentSlot.HEAD, new ItemStack(helmets.get(random.nextInt(6))));
        skeleton.setItemSlot(EquipmentSlot.CHEST, new ItemStack(chestplates.get(random.nextInt(5))));
        skeleton.setItemSlot(EquipmentSlot.LEGS, new ItemStack(leggings.get(random.nextInt(5))));
        skeleton.setItemSlot(EquipmentSlot.FEET, new ItemStack(boots.get(random.nextInt(5))));
    }

    // variations can include:
    // - changing the items in the lists (e.g. adding pumpkins to helmets list)
    // - changing target mob
    // - changing priority of goal (player is priority 2, iron golems and turtles are priority 3)
}
