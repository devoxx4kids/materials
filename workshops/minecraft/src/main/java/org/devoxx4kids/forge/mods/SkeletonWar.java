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

		List<ItemArmor> helmets = Arrays.asList(Items.leather_helmet,
				Items.chainmail_helmet, Items.golden_helmet, Items.iron_helmet,
				Items.diamond_helmet);
		List<ItemArmor> chestplates = Arrays.asList(Items.leather_chestplate,
				Items.chainmail_chestplate, Items.golden_chestplate,
				Items.iron_chestplate, Items.diamond_chestplate);
		List<ItemArmor> leggings = Arrays.asList(Items.leather_leggings,
				Items.chainmail_leggings, Items.golden_leggings,
				Items.iron_leggings, Items.diamond_leggings);
		List<ItemArmor> boots = Arrays.asList(Items.leather_boots,
				Items.chainmail_boots, Items.golden_boots, Items.iron_boots,
				Items.diamond_boots);

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