package org.devoxx4kids.forge.mods;

import net.minecraft.client.Minecraft;
import net.minecraft.init.Items;
import net.minecraft.item.ItemStack;
import net.minecraftforge.client.event.ClientChatReceivedEvent;
import net.minecraftforge.fml.common.eventhandler.SubscribeEvent;

public class ChatItems {

	@SubscribeEvent
	public void giveItems(ClientChatReceivedEvent event) {
		if (event.message.getUnformattedText().contains("diamond")) {
			Minecraft.getMinecraft().thePlayer.inventory.addItemStackToInventory(new ItemStack(Items.diamond, 64));
		}
		
		if (event.message.getUnformattedText().contains("potato")) {
			Minecraft.getMinecraft().thePlayer.inventory.addItemStackToInventory(new ItemStack(Items.potato, 64));
		}
	}
}