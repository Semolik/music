<template>
    <div class="user-playlist-page">
        <Filters v-model:filters="filters" buttonText="Сортировка" />
        <CardsContainer animate>
            <PlaylistCard
                v-for="playlist in playlists"
                :playlist="playlist"
                :key="playlist.id"
                is-link
            />
        </CardsContainer>
        <NotFound v-if="!playlists.length && !fetching" />
        <AppButton v-if="loadMoreButton" active @click="fetchPlaylists">
            Загрузить еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "~/client";
import { useHeaderStore } from "~/stores/header";
const { USER_PLAYLISTS_LIMIT } = useRuntimeConfig().public;
const { id } = useRoute().params;
const user = await Service.getUserInfoByIdApiV1UsersUserIdGet(id);
const headerStore = useHeaderStore();
const fullName = useFullName(user);
headerStore.links = [];
headerStore.setTitle("Плейлисты пользователя " + fullName);
const playlists = ref([]);
var filters = reactive({
    "Сортировать по": {
        values: ["Названию", "Дате создания"],
        active: null,
        default: "Названию",
    },

    "Направление сортировки": {
        values: ["По убыванию", "По возрастанию"],
        active: null,
        default: "По убыванию",
    },
});
const fetching = ref(false);
const page = ref(0);
const loadMoreButton = ref(false);
const fetchPlaylists = async () => {
    fetching.value = true;
    page.value++;
    const items = await Service.getUserPlaylistsApiV1UsersUserIdPlaylistsGet(
        id,
        page.value,
        filters["Сортировать по"].active === "Названию" ? "name" : "created_at",
        filters["Направление сортировки"].active === "По убыванию"
            ? "desc"
            : "asc"
    );
    playlists.value = [...playlists.value, ...items];
    loadMoreButton.value = items.length === USER_PLAYLISTS_LIMIT;
    fetching.value = false;
};

watch(
    filters,
    async () => {
        page.value = 0;
        playlists.value = [];
        await fetchPlaylists();
    },
    { immediate: true }
);
</script>
<style lang="scss" scoped>
.user-playlist-page {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
