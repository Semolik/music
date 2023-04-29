<template>
    <div class="buttons-line">
        <FiltersButton
            @click="filtersMenuOpened = !filtersMenuOpened"
            ref="filtersButton"
        >
            {{ props.buttonText }}
        </FiltersButton>
        <AppSelectFilters
            v-model:filters="filters"
            v-model:filtersMenuOpened="filtersMenuOpened"
            :filtersButton="filtersButton"
            @change="filtersIsActived = $event"
            :head-text="props.buttonText"
        />
        <slot />
    </div>
</template>
<script setup>
const props = defineProps({
    filters: {
        type: Object,
        required: true,
    },
    buttonText: {
        type: String,
        required: false,
        default: "Фильтры",
    },
});
const emit = defineEmits(["update:filters"]);
const filters = computed({
    get: () => props.filters,
    set: (value) => emit("update:filters", value),
});
const filtersButton = ref(null);
const filtersMenuOpened = ref(false);
const filtersIsActived = ref(false);
</script>
<style lang="scss" scoped>
.buttons-line {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    position: relative;
    justify-content: space-between;
}
</style>
