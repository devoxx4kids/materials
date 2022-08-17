package org.devoxx4kids.forge.mods;

import net.minecraft.core.BlockPos;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.event.entity.living.LivingEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = MainMod.MODID)
public class RainWater {
    @SubscribeEvent
    public static void makeWater(LivingEvent.LivingTickEvent event) {
        Entity entity = event.getEntity();
        Level level = entity.level;
        BlockPos entityPos = entity.blockPosition();

        if (level.isClientSide) {
            return;
        }

        if (!level.isRaining() || level.getBiome(entityPos).get().getPrecipitation() != Biome.Precipitation.RAIN) {
            return;
        }

        for (int i = entityPos.getY(); i < 320; i++) {
            if (level.getBlockState(entityPos.atY(i)).getBlock() != Blocks.AIR) {
                return;
            }
        }

        BlockPos posBelow = entityPos.below(1);
        if (!level.getBlockState(posBelow).isCollisionShapeFullBlock(level, posBelow)) {
            return;
        }

        level.setBlockAndUpdate(entityPos, Blocks.WATER.defaultBlockState());
    }

    // TNT thunder
    // ================================

    // @SubscribeEvent
    // public static void spawnTnt(LivingEvent.LivingTickEvent event) {
    //     Entity entity = event.getEntity();
    //     Level level = entity.level;
    //     BlockPos entityPos = entity.blockPosition();
    //
    //     if (level.isClientSide) {
    //         return;
    //     }
    //
    //     if (!level.isThundering() || level.getBiome(entityPos).get().getPrecipitation() != Biome.Precipitation.RAIN) {
    //         return;
    //     }
    //
    //     for (int i = entityPos.getY(); i < 320; i++) {
    //         if (level.getBlockState(entityPos.atY(i)).getBlock() != Blocks.AIR) {
    //             return;
    //         }
    //     }
    //
    //     BlockPos posBelow = entityPos.below(1);
    //     if (!level.getBlockState(posBelow).isCollisionShapeFullBlock(level, posBelow)) {
    //         return;
    //     }
    //
    //     if (level.random.nextInt(40) != 1) {
    //         return;
    //     }
    //
    //     PrimedTnt tnt = EntityType.TNT.create(level);
    //     tnt.setFuse(80);
    //     tnt.moveTo(entityPos, 0, 0);
    //     level.addFreshEntity(tnt);
    // }
}
