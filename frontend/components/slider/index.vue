<template>
    <Swiper
        :modules="[SwiperAutoplay, SwiperEffectCreative]"
        :slides-per-view="1"
        :loop="true"
        :autoplay="{
            delay: 4000,
            disableOnInteraction: true,
        }"
        :style="{
            '--aspect-ratio': $viewport.isGreaterOrEquals('lg')
                ? SLIDER_ASPECT_RATIO_DESKTOP
                : SLIDER_ASPECT_RATIO_MOBILE,
        }"
    >
        <SwiperSlide v-for="slide in slides" :key="slide.id" class="slide">
            <img :src="slide.picture" alt="" />
        </SwiperSlide>
    </Swiper>
</template>
<script setup>
import { Service } from "~~/client";
const { SLIDER_ASPECT_RATIO_DESKTOP, SLIDER_ASPECT_RATIO_MOBILE } =
    useRuntimeConfig().public;

const slides = ref(await Service.getSlidesApiV1SliderGet());
</script>
<style scoped lang="scss">
.slide {
    width: 100%;
    height: 100%;
    aspect-ratio: var(--aspect-ratio);

    img {
        border-radius: 10px;
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}
</style>
