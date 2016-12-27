package org.devoxx4kids.forge.mods;

import java.util.List;

import net.minecraft.entity.monster.EntityCreeper;
import net.minecraft.entity.monster.EntityZombie;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.util.text.TextComponentString;
import net.minecraft.util.text.TextFormatting;
import net.minecraftforge.event.entity.EntityJoinWorldEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class CreeperSpawnAlert {

    @SubscribeEvent
    public void sendAlert(EntityJoinWorldEvent event) {
        if (!(event.getEntity() instanceof EntityCreeper)) {
            return;
        }

        List players = event.getEntity().worldObj.playerEntities;

        for (int i = 0; i < players.size(); i++) {
            EntityPlayer player = (EntityPlayer) players.get(i);
            if (event.getWorld().isRemote) {
                player.addChatComponentMessage(new TextComponentString(TextFormatting.GREEN + "A creeper has spawned!"), false);
            }
        }
    }
}
