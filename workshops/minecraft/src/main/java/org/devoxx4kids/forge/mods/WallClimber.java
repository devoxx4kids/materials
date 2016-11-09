package org.devoxx4kids.forge.mods;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraftforge.event.entity.living.LivingFallEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;
import net.minecraftforge.fml.common.gameevent.TickEvent.PlayerTickEvent;

public class WallClimber {

	@SubscribeEvent
	public void climbWall(PlayerTickEvent event) {

		EntityPlayer player = event.player;

		if (!player.isCollidedHorizontally) {
			return;
		}

		if (player.isActiveItemStackBlocking()) {
			player.motionY = -0.5;
		} else if (player.isSneaking()) {
			player.motionY = 0;
		} else {
			player.motionY = 0.5;
		}

	}

	@SubscribeEvent
	public void negateFallDamage(LivingFallEvent event) {
		if (!(event.getEntity() instanceof EntityPlayer)) {
			return;
		}

		event.setCanceled(true);
	}
}