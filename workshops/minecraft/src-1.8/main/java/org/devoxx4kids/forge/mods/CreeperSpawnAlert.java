package org.devoxx4kids.forge.mods;

import java.util.List;

import net.minecraft.entity.monster.EntityCreeper;
import net.minecraft.entity.monster.EntityZombie;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.util.ChatComponentText;
import net.minecraft.util.EnumChatFormatting;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class CreeperSpawnAlert {

	@SubscribeEvent
	public void sendAlert(EntityJoinWorldEvent event) {
		if (!(event.entity instanceof EntityCreeper || event.entity instanceof EntityZombie)) {
			return;
		}

		String message;

		if (event.entity instanceof EntityCreeper) {
			message = "A creeper has spawned";
		} else {
			message = "A zombie has spawned";
		}

		List players = event.entity.worldObj.playerEntities;

		for (int i = 0; i < players.size(); i++) {
			EntityPlayer player = (EntityPlayer) players.get(i);
			if (event.world.isRemote) {
				player.addChatMessage(new ChatComponentText(
						EnumChatFormatting.GREEN + message));
			}
		}
	}

}