package org.devoxx4kids.forge.mods;

import net.minecraft.entity.boss.EntityDragon;
import net.minecraft.entity.boss.dragon.phase.PhaseList;
import net.minecraft.init.Blocks;
import net.minecraft.util.math.BlockPos;
import net.minecraftforge.event.world.BlockEvent.PlaceEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class DragonSpawner {

	@SubscribeEvent
	public void spawnDragon(PlaceEvent event) {
		if (event.getPlacedBlock() == Blocks.sponge.getBlockState()
				.getBaseState()) {
			event.getWorld().setBlockToAir(
					new BlockPos(event.getPos().getX(), event.getPos().getY(),
							event.getPos().getZ()));
			EntityDragon dragon = new EntityDragon(event.getWorld());
			dragon.setLocationAndAngles(event.getPos().getX(), event.getPos()
					.getY(), event.getPos().getZ(), 0, 0);
			dragon.getPhaseManager().setPhase(PhaseList.TAKEOFF);
			event.getWorld().spawnEntityInWorld(dragon);
		}
	}
}