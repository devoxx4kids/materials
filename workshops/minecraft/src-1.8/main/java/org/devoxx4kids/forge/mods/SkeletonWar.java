package org.devoxx4kids.forge.mods;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

import net.minecraft.entity.ai.EntityAINearestAttackableTarget;
import net.minecraft.entity.monster.EntityMob;
import net.minecraft.entity.monster.EntitySkeleton;
import net.minecraft.init.Items;
import net.minecraft.item.ItemArmor;
import net.minecraft.item.ItemStack;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class SkeletonWar {

	@SubscribeEvent
	public void makeWarNotPeace(EntityJoinWorldEvent event) {
		if (!(event.entity instanceof EntityMob)) {
			return;
		}
		EntityMob entity = (EntityMob) event.entity;

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

		entity.targetTasks.addTask(3, new EntityAINearestAttackableTarget(
				entity, EntityMob.class, true));
		entity.canPickUpLoot();

		Random random = new Random();
		entity.setCurrentItemOrArmor(4,
				new ItemStack(helmets.get(random.nextInt(5))));
		entity.setCurrentItemOrArmor(3,
				new ItemStack(chestplates.get(random.nextInt(5))));
		entity.setCurrentItemOrArmor(2,
				new ItemStack(leggings.get(random.nextInt(5))));
		entity.setCurrentItemOrArmor(1,
				new ItemStack(boots.get(random.nextInt(5))));
	}

}