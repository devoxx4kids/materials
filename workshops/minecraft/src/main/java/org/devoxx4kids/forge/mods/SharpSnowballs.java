package org.devoxx4kids.forge.mods;

import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.projectile.Arrow;
import net.minecraft.world.entity.projectile.Snowball;
import net.minecraft.world.level.Level;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = MainMod.MODID)
public class SharpSnowballs {
    @SubscribeEvent
    public static void replaceSnowballWithArrow(EntityJoinLevelEvent event) {
        Entity snowball = event.getEntity();
        Level level = event.getLevel();

        if (!(snowball instanceof Snowball)) {
            return;
        }

        if (!level.isClientSide) {
            Arrow arrow = EntityType.ARROW.create(level);
            arrow.moveTo(snowball.position());
            arrow.setDeltaMovement(snowball.getDeltaMovement());
            level.addFreshEntity(arrow);
        }

        event.setCanceled(true);
    }

    // explosive snowballs
    // ================================

    // @SubscribeEvent
    // public static void replaceSnowballWithArrow(EntityJoinLevelEvent event) {
    //     Entity snowball = event.getEntity();
    //     Level level = event.getLevel();
    //
    //     if (!(snowball instanceof Snowball)) {
    //         return;
    //     }
    //
    //     if (!level.isClientSide) {
    //         PrimedTnt tnt = EntityType.TNT.create(level);
    //         tnt.setFuse(80);
    //         tnt.moveTo(snowball.position());
    //         tnt.setDeltaMovement(snowball.getDeltaMovement());
    //         level.addFreshEntity(tnt);
    //     }
    //
    //     event.setCanceled(true);
    // }
}
