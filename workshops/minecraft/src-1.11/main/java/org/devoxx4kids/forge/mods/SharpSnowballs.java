package org.devoxx4kids.forge.mods;

import net.minecraft.entity.Entity;
import net.minecraft.entity.item.EntityTNTPrimed;
import net.minecraft.entity.projectile.EntitySnowball;
import net.minecraft.entity.projectile.EntityTippedArrow;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class SharpSnowballs {

	@SubscribeEvent
	public void replaceSnowballWithArrow(EntityJoinWorldEvent event) {
		Entity snowball = event.getEntity();
		World world = snowball.worldObj;

		if (!(snowball instanceof EntitySnowball)) {
			return;
		}

		if (!world.isRemote) {
			EntityTippedArrow arrow = new EntityTippedArrow(world);
			arrow.setLocationAndAngles(snowball.posX, snowball.posY, snowball.posZ,
					0, 0);
			arrow.motionX = snowball.motionX;
			arrow.motionY = snowball.motionY;
			arrow.motionZ = snowball.motionZ;

			// gets arrow out of player's head
			// gets the angle of arrow right, in the direction of motion
			arrow.posX += arrow.motionX;
			arrow.posY += arrow.motionY;
			arrow.posZ += arrow.motionZ;

			world.spawnEntityInWorld(arrow);
			snowball.setDead();
		}
	}
}