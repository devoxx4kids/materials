package org.devoxx4kids.forge.mods;

import java.util.Random;

import net.minecraft.client.Minecraft;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.projectile.EntityArrow;
import net.minecraft.entity.projectile.EntityArrow.PickupStatus;
import net.minecraft.entity.projectile.EntitySpectralArrow;
import net.minecraft.entity.projectile.EntityTippedArrow;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class ArrowShotgun {

	private final int arrows = 20;

	@SubscribeEvent
	public void shootArrows(EntityJoinWorldEvent event) {
		EntityPlayer player = Minecraft.getMinecraft().thePlayer;
		World world = event.world;

		if (!(event.entity instanceof EntitySpectralArrow)){
			return;
		}
		
		if(player.isEntityEqual(((EntityArrow)event.entity).shootingEntity)){
			return;
		}

		Random random = new Random();

		for (int i = 0; i < arrows; i++) {
			EntityArrow arrow = new EntityTippedArrow(world, player);
			arrow.setVelocity(event.entity.motionX, event.entity.motionY, event.entity.motionZ);
			arrow.posX += arrow.motionX + random.nextFloat() - 0.5F;
			arrow.posY += arrow.motionY + random.nextFloat() - 0.5F;
			arrow.posZ += arrow.motionZ + random.nextFloat() - 0.5F;
			arrow.canBePickedUp = PickupStatus.DISALLOWED;
			arrow.setFire(10000);
			if (!world.isRemote) {
				world.spawnEntityInWorld(arrow);
			}
		}
		event.entity.setDead();
	}
}