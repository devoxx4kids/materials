package org.devoxx4kids.forge.mods;

import net.minecraft.entity.EntityLiving;
import net.minecraft.entity.monster.EntityIronGolem;
import net.minecraft.potion.PotionEffect;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class OverpoweredIronGolems {

	@SubscribeEvent
	public void golemMagic(EntityJoinWorldEvent event) {
		if (!(event.entity instanceof EntityIronGolem)) {
			return;
		}

		EntityLiving entity = (EntityLiving) event.entity;
		entity.addPotionEffect(new PotionEffect(2, 1000000, 5));
		entity.addPotionEffect(new PotionEffect(18, 1000000, 5));
		entity.addPotionEffect(new PotionEffect(19, 1000000, 5));
		entity.addPotionEffect(new PotionEffect(20, 1000000, 5));
	}

}