package org.devoxx4kids.forge.mods;

import net.minecraft.entity.Entity;
import net.minecraft.init.Blocks;
import net.minecraft.util.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.event.entity.living.LivingEvent.LivingUpdateEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class RainWater {

	@SubscribeEvent
	public void makeWater(LivingUpdateEvent event) {
		Entity entity = event.entity;
		World world = entity.worldObj;
		int x = (int) Math.floor(entity.posX);
		int y = (int) Math.floor(entity.posY);
		int z = (int) Math.floor(entity.posZ);

		if (!entity.worldObj.isRaining()) {
			return;
		}

		for (int i = y; i < 256; i++) {
			if (world.getBlockState(new BlockPos(x, i, z)) != Blocks.air.getBlockState().getBaseState()) {
				return;
			}
		}

		if (world.isRemote || !world.getBlockState(new BlockPos(x, y - 1, z)).getBlock().isNormalCube()) {
			return;
		}

		world.setBlockState(new BlockPos(x, y, z), Blocks.web.getBlockState().getBaseState());
	}

}