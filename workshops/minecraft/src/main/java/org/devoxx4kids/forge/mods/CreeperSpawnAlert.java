package org.devoxx4kids.forge.mods;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.monster.Creeper;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = MainMod.MODID)
public class CreeperSpawnAlert {
    @SubscribeEvent
    public static void sendAlert(EntityJoinLevelEvent event) {
        if (!(event.getEntity() instanceof Creeper)) {
            return;
        }

        if (!event.getLevel().isClientSide) {
            return;
        }

        for (Player player : event.getLevel().players()) {
            player.sendSystemMessage(Component.literal(ChatFormatting.GREEN + "A creeper has spawned!"));
        }
    }

    // variations are pretty simple
    // EntityCreeper becomes Creeper, EntityZombie becomes Zombie, etc.
}
