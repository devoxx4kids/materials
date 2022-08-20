package com.example.examplemod;

import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraftforge.event.ServerChatEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = ExampleMod.MODID)
public class ChatItems {
    @SubscribeEvent
    public static void giveItems(ServerChatEvent event) {
        if (event.getMessage().contains("potato")) {
            event.getPlayer().getInventory().add(new ItemStack(Items.POTATO, 64));
        }

//        if (event.getMessage().contains("diamond")) {
//            event.getPlayer().getInventory().add(new ItemStack(Items.DIAMOND, 64));
//        }
    }

    // multiple items
    // ================================

//     @SubscribeEvent
//     public static void giveItems(ServerChatEvent event) {
//         if (event.getMessage().contains("potato")) {
//             event.getPlayer().getInventory().add(new ItemStack(Items.POTATO, 64));
//             event.getPlayer().getInventory().add(new ItemStack(Items.DIAMOND, 64));
//         }
//     }
}
