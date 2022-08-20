package com.example.examplemod;

import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.monster.Creeper;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.entity.player.Player;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = ExampleMod.MODID)
public class CreeperSpawnAlert {
    @SubscribeEvent
    public static void sendAlert(EntityJoinLevelEvent event) {
        if (event.getEntity() instanceof Creeper && event.getLevel().isClientSide) {
            for (Player player : event.getLevel().players()) {
                player.sendSystemMessage(Component.literal(ChatFormatting.RED + "A creeper has spawned!"));
            }
        }
//        if (event.getEntity() instanceof Zombie && event.getLevel().isClientSide) {
//            for (Player player : event.getLevel().players()) {
//                player.sendSystemMessage(Component.literal(ChatFormatting.GREEN + "A zombie has spawned!"));
//            }
//        }
    }
}

