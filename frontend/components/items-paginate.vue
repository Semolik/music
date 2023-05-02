<template>
    <CardsContainer v-bind="$attrs">
        <slot :items="items" />
        <NotFound v-if="!items.length && !fetching" />
        <AppButton v-if="loadMoreButton">Загрузить еще</AppButton>
    </CardsContainer>
</template>
<script setup>
const { onNextPage, page_size } = defineProps({
    onNextPage: {
        type: Function,
        required: true,
    },
    pageSize: {
        type: Number,
        required: true,
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
    loadMoreButton.value = new_items.length == page_size;
    fetching.value = false;
};
loadMore();
</script>
