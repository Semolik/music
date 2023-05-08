<template>
    <div class="favorite-page-container">
        <Filters v-model:filters="filters">
            <FiltersButton @click="createPlaylistModalOpened = true">
                Создать плейлист
            </FiltersButton>
        </Filters>

        <ModalDialog
            @close="createPlaylistModalOpened = false"
            :active="createPlaylistModalOpened"
        >
            <template #content>
                <PlaylistCreateModalContent @creared="onCreatedPlaylist" />
            </template>
        </ModalDialog>
        <CardsContainer>
            <PlaylistCard
                v-for="playlist in playlists"
                :playlist="playlist"
                :key="playlist.id"
                is-link
            />
        </CardsContainer>
        <AppButton v-if="loadMoreButton" active @click="getPlaylists">
            Загрузить еще
        </AppButton>
        <NotFound
            :text="
                filtersIsActived
                    ? 'По вашему запросу ничего не найдено'
                    : 'У вас нет плейлистов'
            "
            v-if="!playlists.length && !fething"
        />
    </div>
</template>
<script setup>
import { Service } from "@/client";
const filtersIsActived = ref(false);
const createPlaylistModalOpened = ref(false);
const { USER_PLAYLISTS_LIMIT } = useRuntimeConfig().public;
const loadMoreButton = ref(false);
var filters = reactive({
    "Сортировать по": {
        values: ["Названию", "Дате добавления"],
        active: null,
        default: "Названию",
    },
    Тип: {
        values: ["Все", "Приватные"],
        active: null,
        default: "Все",
    },
    Создатель: {
        values: ["Все", "Мои"],
        active: null,
        default: "Все",
        disabled: false,
    },
    "Направление сортировки": {
        values: ["По убыванию", "По возрастанию"],
        active: null,
        default: "По убыванию",
    },
});
const fething = ref(false);
const playlists = ref([]);
const page = ref(0);
const getPlaylists = async () => {
    if (fething.value) return;
    page.value++;
    fething.value = true;
    const order_by =
        filters["Сортировать по"].active === "Названию" ? "name" : "created_at";
    const order =
        filters["Направление сортировки"].active === "По возрастанию"
            ? "asc"
            : "desc";
    const owned_only = filters["Создатель"].active === "Мои" ? true : false;
    const private_ = filters["Тип"].active === "Приватные" ? true : false;
    const new_playlists = await Service.getMyPlaylistsApiV1PlaylistsGet(
        order_by,
        order,
        owned_only,
        private_
    );
    playlists.value = [...playlists.value, ...new_playlists];
    loadMoreButton.value = new_playlists.length === USER_PLAYLISTS_LIMIT;
    fething.value = false;
};

watch(
    filters,
    async (value) => {
        page.value = 0;
        playlists.value = [];
        if (value["Тип"].active === "Приватные") {
            value["Создатель"].disabled = true;
            value["Создатель"].active = "Мои";
        } else {
            value["Создатель"].disabled = false;
        }

        await getPlaylists();
    },
    { immediate: true }
);

const onCreatedPlaylist = async (playlist) => {
    createPlaylistModalOpened.value = false;
    fething.value = true;
    playlists.value.unshift(playlist);
    fething.value = false;
};
</script>
<style lang="scss" scoped>
.favorite-page-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
}
</style>
