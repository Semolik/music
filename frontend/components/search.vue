<template>
    <AppInput
        placeholder="Введите запрос"
        v-model="searchQuery"
        size="large"
        :suffix-icon="searching ? Loading : null"
        clearable
        id="search-input"
    />
    <div class="results-categories" v-if="searchQuery">
        <div
            :class="['results-categories-item', { active: category === key }]"
            @click="category = key"
            v-for="(_, key) in results"
        >
            {{ categoriesNames[key] }}
        </div>
    </div>
    <div
        :class="['results', category, { tracks: category == 'tracks' }]"
        v-if="isFound"
    >
        <template v-if="category === 'all'">
            <template v-for="item in results.all">
                <AlbumCard v-if="item.type == 'album'" :album="item.info" min />
                <MusicianCard
                    v-if="item.type == 'musician'"
                    :musician="item.info"
                />
                <TrackCard
                    v-if="item.type == 'track'"
                    :track="item.info"
                    min
                    hide-dots-menu
                />
                <PlaylistCard
                    v-if="item.type == 'playlist'"
                    :playlist="item.info"
                    min
                />
            </template>
        </template>
        <template v-if="category === 'musicians'">
            <MusicianCard
                v-for="artist in results.musicians"
                :musician="artist"
            />
        </template>
        <template v-if="category === 'tracks'">
            <TrackCard
                v-for="(track, index) in results.tracks"
                v-model:track="results.tracks[index]"
                hide-dots-menu
                min
            />
        </template>
        <template v-if="category === 'albums'">
            <AlbumCard v-for="album in results.albums" :album="album" />
        </template>
        <template v-if="category === 'playlists'">
            <PlaylistCard
                v-for="playlist in results.playlists"
                :playlist="playlist"
            />
        </template>
    </div>
    <div class="not-found" v-else-if="searchQuery">
        по вашему запросу ничего не найдено
    </div>
    <div class="recomendations" v-else>рекомендации</div>
</template>
<script setup>
import { Service } from "@/client";
import { Loading } from "@element-plus/icons-vue";
import { useEventBus } from "@vueuse/core";

const resetSearchBus = useEventBus("reset-search");
const results = reactive({
    all: [],
    albums: [],
    musicians: [],
    playlists: [],
    tracks: [],
});
const category = ref("all");
const searching = ref(false);
const isFound = computed(
    () => results[category.value] && results[category.value].length > 0
);

const categoriesNames = {
    all: "Топ",
    albums: "Альбомы",
    musicians: "Исполнители",
    playlists: "Плейлисты",
    tracks: "Треки",
};

const searchQuery = ref("");
watch([searchQuery, category], async ([val, category]) => {
    if (!val) {
        for (const key in results) {
            results[key] = [];
        }
        searching.value = false;
        return;
    }
    searching.value = true;
    switch (category) {
        case "all":
            const result_all = await Service.searchApiV1SearchAutocompleteGet(
                val
            );
            results.all = result_all;
            searching.value = false;
            break;
        case "musicians":
            const result_musicians =
                await Service.searchMusicianApiV1SearchMusicianGet(val);
            results.musicians = result_musicians;
            searching.value = false;
            break;
        case "albums":
            const result_albums = await Service.searchAlbumApiV1SearchAlbumGet(
                val
            );
            results.albums = result_albums;
            searching.value = false;
            break;
        case "tracks":
            const result_tracks = await Service.searchTrackApiV1SearchTrackGet(
                val
            );
            results.tracks = result_tracks;
            searching.value = false;
            break;
        case "playlists":
            const result_playlists =
                await Service.searchPlaylistApiV1SearchPlaylistGet(val);
            results.playlists = result_playlists;
            searching.value = false;
            break;
    }
});

const resetSearch = () => {
    searchQuery.value = "";
    category.value = "all";
    for (const key in results) {
        results[key] = [];
    }
};
const unsubscribe = resetSearchBus.on(resetSearch);

onBeforeUnmount(() => {
    unsubscribe();
});
</script>

<style lang="scss">
.results-categories {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;

    .results-categories-item {
        @include flex-center;
        gap: 10px;
        flex-grow: 1;
        padding: 5px 20px;
        border-radius: 5px;
        background-color: $quinary-bg;
        white-space: nowrap;
        cursor: pointer;
        user-select: none;
        border: 1px solid transparent;
        color: $primary-text;
        &:not(.active):hover {
            background-color: $quaternary-bg;
        }
        &.active {
            border-color: $accent;
            cursor: auto;
        }
    }
}
.results {
    height: 100%;
    transition: 0.3s ease all;
    display: flex;
    flex-direction: column;
    gap: 10px;
    overflow-y: auto;
    overflow-x: hidden;

    &.all {
        .results-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 5px;
            height: 70px;
        }
    }
    &:not(.all) {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));

        &.tracks {
            grid-template-columns: 1fr;
        }
    }
}
.not-found {
    @include flex-center;
    height: 100%;
    color: $secondary-text;
    flex-grow: 1;
}
#search-input {
    --app-input-bg: transparent;
    --app-input-border-radius: 5px;
    &.el-input--large {
        .el-input__inner {
            font-size: large;
        }
    }
    .el-input__wrapper {
        .el-input__suffix {
            .el-icon:not(.el-input__clear) {
                svg {
                    @keyframes rotate {
                        0% {
                            transform: rotate(0deg);
                        }
                        100% {
                            transform: rotate(360deg);
                        }
                    }
                    animation: rotate 1s linear infinite;
                }
            }
        }
    }
}
</style>
