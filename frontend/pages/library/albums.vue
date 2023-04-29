<template>
    <div class="albums-page-container">
        <Filters v-model:filters="filters" button-text="Сортировка" />
        <CardsContainer>
            <AlbumCard v-for="album in albums" :album="album" is-link />
        </CardsContainer>
        <AppButton
            v-if="loadMoreButton"
            @click="loadMore"
            :loading="fething"
            active
        >
            Загрузить еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "@/client";
const { FAVORITE_ALBUMS_LIMIT } = useRuntimeConfig().public;
const albums = ref([]);
const page = ref(1);
const loadMoreButton = ref(false);
const fething = ref(false);

var filters = reactive({
    "Сортировать по": {
        values: ["Названию", "Дате добавления", "Популярности"],
        active: null,
        default: "Дате добавления",
    },
    "Направление сортировки": {
        values: ["По убыванию", "По возрастанию"],
        active: null,
        default: "По убыванию",
    },
});
const order_by = computed(() => {
    switch (filters["Сортировать по"].active) {
        case "Названию":
            return "name";
        case "Дате добавления":
            return "date";
        case "Популярности":
            return "likes";
    }
});
const order = computed(() =>
    filters["Направление сортировки"].active === "По возрастанию"
        ? "asc"
        : "desc"
);
const getAlbums = async () => {
    fething.value = true;
    const newAlbums = await Service.getLikedAlbumsApiV1AlbumsLikedGet(
        order_by.value,
        order.value,
        page.value
    );
    albums.value = albums.value.concat(newAlbums);
    loadMoreButton.value = newAlbums.length == FAVORITE_ALBUMS_LIMIT;
    fething.value = false;
};
const loadMore = async () => {
    page.value++;
    await getAlbums();
};
watch(
    filters,
    async (value) => {
        albums.value = [];
        page.value = 1;
        loadMoreButton.value = false;
        await getAlbums();
    },
    { immediate: true }
);
</script>
<style lang="scss" scoped>
.albums-page-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    color: $primary-text;
}
</style>
