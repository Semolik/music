<template>
    <Swiper
        :modules="[SwiperAutoplay, SwiperEffectCreative]"
        :slides-per-view="1"
        :loop="true"
        :effect="'creative'"
        :autoplay="{
            delay: 8000,
            disableOnInteraction: true,
        }"
        :style="{
            '--aspect-ratio': SLIDER_ASPECT_RATIO,
        }"
        :creative-effect="{
            prev: {
                shadow: false,
                translate: ['-20%', 0, -1],
            },
            next: {
                translate: ['100%', 0, 0],
            },
        }"
    >
        <SwiperSlide v-for="slide in slides" :key="slide.id" class="slide">
            <img :src="slide.picture" alt="" />
        </SwiperSlide>
    </Swiper>
</template>
<script setup>
import { Service } from "~~/client";
const { SLIDER_ASPECT_RATIO } = useRuntimeConfig().public;

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
