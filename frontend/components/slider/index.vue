<template>
    <Swiper
        :modules="[SwiperAutoplay, SwiperEffectCreative]"
        :slides-per-view="1"
        :loop="true"
        :autoplay="{
            delay: 4000,
            disableOnInteraction: true,
        }"
        :spaceBetween="10"
        :style="{
            '--aspect-ratio': SLIDER_ASPECT_RATIO,
        }"
    >
        <SwiperSlide v-for="slide in slides" :key="slide.id" class="slide">
            <a :href="slide.url">
                <img :src="slide.picture" />
            </a>
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
