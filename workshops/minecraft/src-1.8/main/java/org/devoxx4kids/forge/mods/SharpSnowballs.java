package org.devoxx4kids.forge.mods;

import net.minecraft.entity.Entity;
import net.minecraft.entity.item.EntityTNTPrimed;
import net.minecraft.entity.projectile.EntityArrow;
import net.minecraft.entity.projectile.EntitySnowball;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class SharpSnowballs {

	@SubscribeEvent
	public void replaceSnowballWithArrow(EntityJoinWorldEvent event) {
		Entity snowball = event.entity;
		World world = snowball.worldObj;

		if (!(snowball instanceof EntitySnowball)) {
			return;
		}

		if (!world.isRemote) {
			EntityTNTPrimed tnt = new EntityTNTPrimed(world);
			tnt.fuse = 80;
			tnt.setLocationAndAngles(snowball.posX, snowball.posY, snowball.posZ,
					0, 0);
			tnt.motionX = snowball.motionX;
			tnt.motionY = snowball.motionY;
			tnt.motionZ = snowball.motionZ;

			// gets arrow out of player's head
			// gets the angle of arrow right, in the direction of motion
			tnt.posX += tnt.motionX;
			tnt.posY += tnt.motionY;
			tnt.posZ += tnt.motionZ;

			world.spawnEntityInWorld(tnt);
			snowball.setDead();
		}
	}

}