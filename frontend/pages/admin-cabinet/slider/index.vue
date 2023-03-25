<template>
    <div class="slides-page">
        <AppButton
            border-radius="5px"
            active
            @click="$router.push('/admin-cabinet/slider/new')"
        >
            Добавить слайд
        </AppButton>
        <div class="slides-container">
            <SliderCard
                v-for="slide in slides"
                :key="slide.id"
                :slide="slide"
            />
        </div>
        <AppButton v-if="showButton" @click="loadMore" active>
            Загрузить еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "~~/client";

definePageMeta({
    middleware: ["admin"],
});
const runtimeConfig = useRuntimeConfig();
const { SLIDER_PAGE_ITEMS } = runtimeConfig.public;
const page = ref(1);
const slides = ref(await Service.getAllSlidesApiV1SliderAllGet(page.value));
const showButton = ref(slides.value.length === SLIDER_PAGE_ITEMS);
const loadMore = async () => {
    page.value++;
    const newSlides = await Service.getAllSlidesApiV1SliderAllGet(page.value);
    slides.value = [...slides.value, ...newSlides];
    showButton.value = newSlides.length === SLIDER_PAGE_ITEMS;
};
</script>
<style lang="scss" scoped>
.slides-page {
    display: flex;
    flex-direction: column;

    .slides-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 10px;
    }
}
</style>
