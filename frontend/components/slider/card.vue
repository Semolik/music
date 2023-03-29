<template>
    <nuxt-link
        class="slide"
        :key="slide.id"
        :to="{
            name: routesNames.adminCabinet.cabinetSliderId,
            params: { id: slide.id },
        }"
    >
        <div class="line">
            <div class="name">
                {{ slide.name }}
            </div>
            <div class="small" v-if="slide.order !== null">
                Порядок: {{ slide.order }}
            </div>
        </div>
        <div class="line">
            <div class="dates">
                <div class="date">
                    {{ startDate }}
                </div>
                -
                <div class="date">
                    {{ endDate }}
                </div>
            </div>
            <div class="small" v-if="!slide.is_active">Деактивирован</div>
        </div>
    </nuxt-link>
</template>
<script setup>
import { routesNames } from "@typed-router";
import moment from "moment";
const { slide } = defineProps({
    slide: {
        type: Object,
        required: true,
    },
});
const startDate = computed(() =>
    moment(slide.active_from).format("DD.MM.YYYY h:mm")
);
const endDate = computed(() =>
    slide.active_to ? moment(slide.active_to).format("DD.MM.YYYY") : "Бессрочно"
);
</script>
<style scoped lang="scss">
.slide {
    display: grid;
    gap: 5px;
    padding: 10px;
    background-color: $quaternary-bg;
    border-radius: 5px;

    &:hover {
        background-color: $quinary-bg;
    }

    .line {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;

        .small {
            font-size: 14px;
            color: $secondary-text;
        }
    }
    .dates {
        display: flex;
        gap: 5px;
        align-items: center;
        font-size: 14px;
        color: $secondary-text;
    }
}
</style>
