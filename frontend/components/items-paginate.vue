<template>
    <CardsContainer v-bind="$attrs" v-if="!isTracks">
        <slot :items="items" />
        <NotFound v-if="!items.length && !fetching" />
        <AppButton v-if="loadMoreButton">Загрузить еще</AppButton>
    </CardsContainer>
    <TracksContainer v-else v-bind="$attrs">
        <slot :items="items" />
        <NotFound v-if="!items.length && !fetching" />
        <AppButton v-if="loadMoreButton">Загрузить еще</AppButton>
    </TracksContainer>
</template>
<script setup>
const { onNextPage, pageSize, isTracks } = defineProps({
    onNextPage: {
        type: Function,
        required: true,
    },
    pageSize: {
        type: Number,
        required: true,
    },
    isTracks: {
        type: Boolean,
        default: false,
    },
});

const items = ref([]);
const page = ref(0);
const loadMoreButton = ref(false);
const fetching = ref(false);
const loadMore = async () => {
    fetching.value = true;
    page.value++;
    const new_items = await onNextPage(page.value);
    items.value = items.value.concat(new_items);
    loadMoreButton.value = new_items.length == pageSize;
    fetching.value = false;
};
loadMore();
</script>
