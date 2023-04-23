<template>
    <Swiper
        :modules="[SwiperAutoplay, SwiperEffectCreative]"
        v-bind="$attrs"
        :slides-per-view="1"
        :loop="loop"
        :autoplay="
            autoplay ? { delay: 4000, disableOnInteraction: true } : false
        "
    >
        <slot />
    </Swiper>
</template>
<script setup>
defineProps({
    autoplay: {
        type: Boolean,
        default: true,
    },
    loop: {
        type: Boolean,
        default: true,
    },
});
</script>
<style lang="scss">
.swiper {
    .swiper-button-next,
    .swiper-button-prev {
        @include flex-center;
        padding: 10px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background-color: rgba(0, 0, 0, 0.5);
    }
}
</style>
