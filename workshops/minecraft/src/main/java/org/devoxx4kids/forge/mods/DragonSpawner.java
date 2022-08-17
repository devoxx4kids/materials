package org.devoxx4kids.forge.mods;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.boss.enderdragon.EnderDragon;
import net.minecraft.world.entity.boss.enderdragon.phases.EnderDragonPhase;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.event.level.BlockEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = MainMod.MODID)
public class DragonSpawner {
    @SubscribeEvent
    public static void spawnDragon(BlockEvent.EntityPlaceEvent event) {
        if (event.getPlacedBlock().getBlock() == Blocks.DRAGON_EGG) {
            event.getLevel().removeBlock(event.getPos(), false); // false = no flags
            EnderDragon dragon = EntityType.ENDER_DRAGON.create(event.getEntity().getLevel());
            dragon.moveTo(event.getPos(), 0, 0);
            dragon.getPhaseManager().setPhase(EnderDragonPhase.TAKEOFF);
            event.getLevel().addFreshEntity(dragon);
        }
    }

    // spawn squid
    // ================================

    // @SubscribeEvent
    // public static void spawnSquid(BlockEvent.EntityPlaceEvent event) {
    //     if (event.getPlacedBlock() == Blocks.SPONGE.defaultBlockState()) {
    //         event.getLevel().removeBlock(event.getPos(), false); // false = no flags
    //         Squid squid = EntityType.SQUID.create(event.getEntity().level);
    //         squid.moveTo(event.getPos(), 0, 0);
    //         event.getLevel().addFreshEntity(squid);
    //     }
    // }

    // position offset
    // ================================

    // @SubscribeEvent
    // public static void spawnDragon(BlockEvent.EntityPlaceEvent event) {
    //     if (event.getPlacedBlock() == Blocks.DRAGON_EGG.defaultBlockState()) {
    //         event.getLevel().removeBlock(event.getPos(), false); // false = no flags
    //         EnderDragon dragon = EntityType.ENDER_DRAGON.create(event.getEntity().level);
    //         dragon.moveTo(event.getPos().above(5), 0, 0);
    //         dragon.getPhaseManager().setPhase(EnderDragonPhase.TAKEOFF);
    //         event.getLevel().addFreshEntity(dragon);
    //     }
    // }
}
