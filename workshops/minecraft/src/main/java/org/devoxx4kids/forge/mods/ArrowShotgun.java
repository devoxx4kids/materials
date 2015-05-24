package org.devoxx4kids.forge.mods;

import java.util.Random;

import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.projectile.EntityArrow;
import net.minecraft.init.Items;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.player.PlayerInteractEvent;
import net.minecraftforge.event.entity.player.PlayerInteractEvent.Action;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class ArrowShotgun {

	private final int arrows = 20;

	@SubscribeEvent
	public void shootArrows(PlayerInteractEvent event) {
		EntityPlayer player = event.entityPlayer;
		World world = event.world;

		if (player.getHeldItem() == null) {
			return;
		}

		if ((event.action != Action.RIGHT_CLICK_AIR && event.action != Action.RIGHT_CLICK_BLOCK)
				|| player.getHeldItem().getItem() != Items.stick) {
			return;
		}

		Random random = new Random();

		for (int i = 0; i < arrows; i++) {
			EntityArrow arrow = new EntityArrow(world, player, 2);
			arrow.posX += arrow.motionX + random.nextFloat() - 0.5F;
			arrow.posY += arrow.motionY + random.nextFloat() - 0.5F;
			arrow.posZ += arrow.motionZ + random.nextFloat() - 0.5F;
			arrow.canBePickedUp = 0;
			arrow.setFire(10000);
			if (!world.isRemote) {
				world.spawnEntityInWorld(arrow);
			}
		}
	}
}