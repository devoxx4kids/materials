package org.devoxx4kids.forge.mods;

import net.minecraft.entity.boss.EntityDragon;
import net.minecraft.entity.passive.EntitySquid;
import net.minecraft.init.Blocks;
import net.minecraft.util.BlockPos;
import net.minecraftforge.event.world.BlockEvent.PlaceEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class DragonSpawner {

	@SubscribeEvent
	public void spawnDragon(PlaceEvent event) {
		if (event.placedBlock == Blocks.sponge.getBlockState().getBaseState()) {
			event.world.setBlockToAir(new BlockPos(event.pos.getX(), event.pos.getY(), event.pos.getZ()));
			EntitySquid squid = new EntitySquid(event.world);
			squid.setLocationAndAngles(event.pos.getX(), event.pos.getY(), event.pos.getZ(), 0, 0);
			event.world.spawnEntityInWorld(squid);
		}
	}
}