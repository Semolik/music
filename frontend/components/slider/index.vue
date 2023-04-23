<template>
    <div class="slider-container" v-if="slides.length">
        <SliderSwiper
            :style="{
                '--aspect-ratio': SLIDER_ASPECT_RATIO,
            }"
        >
            <SwiperSlide v-for="slide in slides" :key="slide.id" class="slide">
                <a :[slide.url&&`href`]="slide.url">
                    <img :src="slide.picture" />
                </a>
            </SwiperSlide>
        </SliderSwiper>
    </div>
</template>
<script setup>
import { Service } from "~~/client";
const { SLIDER_ASPECT_RATIO } = useRuntimeConfig().public;

const slides = await Service.getSlidesApiV1SliderGet();
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
