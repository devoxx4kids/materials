package org.devoxx4kids.forge.mods;

import net.minecraft.entity.boss.EntityDragon;
import net.minecraft.init.Blocks;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.event.world.BlockEvent.PlaceEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class DragonSpawner {

	@SubscribeEvent
	public void spawnDragon(PlaceEvent event) {
		if (event.placedBlock == Blocks.dragon_egg.getBlockState().getBaseState()) {
			event.world.setBlockToAir(new BlockPos(event.pos.getX(), event.pos.getY(), event.pos.getZ()));
			EntityDragon dragon = new EntityDragon(event.world);
			dragon.setLocationAndAngles(event.pos.getX(), event.pos.getY(), event.pos.getZ(), 0, 0);
			event.world.spawnEntityInWorld(dragon);
		}
	}
}