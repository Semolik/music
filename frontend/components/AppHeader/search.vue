<template>
    <ModalDialog
        :active="props.searchActive"
        @update:active="onSearchActiveUpdate"
        id="search-modal"
        :max-width="800"
        :max-height="600"
        off-justify-content
        @mounted="focus"
        @close="resetSearch"
    >
        <template #header>
            <span class="font-medium mb-2 p-2 text-center">
                Поиск по трекам, альбомам, клипам, исполнителям и плейлистам
            </span>
        </template>
        <template #content>
            <el-input
                placeholder="Введите запрос"
                v-model="searchQuery"
                size="large"
                ref="searchInput"
            />
            <div
                :class="['results-categories']"
                v-if="searchQuery && category !== 'all'"
            >
                <div
                    :class="['back-button', { active: category === 'all' }]"
                    @click="category = 'all'"
                >
                    <Icon name="material-symbols:arrow-back-rounded" />
                    <span>Назад</span>
                </div>
                <div class="current-category">
                    {{ categoriesNames[category] }}
                </div>
            </div>

            <div class="results" v-if="hasResults">
                <template v-if="results.musicians">
                    <div
                        class="results-item-title"
                        v-if="category === 'all'"
                        @click="category = 'musicians'"
                    >
                        <span>{{ categoriesNames["musicians"] }}</span>
                        <Icon name="material-symbols:arrow-forward-rounded" />
                    </div>
                    <div
                        v-if="['all', 'musicians'].includes(category)"
                        class="results-item musicians"
                    >
                        <MusicianCard
                            v-for="artist in results.musicians"
                            :key="artist.id"
                            :musician="artist"
                        />
                    </div>
                </template>
            </div>
        </template>
    </ModalDialog>
</template>

<script setup>
import { Service } from "@/client";

const emit = defineEmits(["update:searchActive"]);
const props = defineProps({
    searchActive: {
        type: Boolean,
        default: false,
    },
});
const searchInput = ref(null);
const results = reactive({
    albums: null,
    musicians: null,
    playlists: null,
    tracks: null,
});
const categoriesNames = {
    albums: "Альбомы",
    musicians: "Исполнители",
    playlists: "Плейлисты",
    tracks: "Треки",
};
const hasResults = computed(() => {
    for (const key in results) {
        if (results[key]) {
            return true;
        }
    }
    return false;
});
const focus = () => {
    const input = searchInput.value;
    if (input) {
        input.focus();
    }
};
const resetSearch = () => {
    searchQuery.value = "";
    category.value = "all";
    for (const key in results) {
        results[key] = null;
    }
};
const category = ref("all");
const searchQuery = ref("");
watch([searchQuery, category], async ([val, category]) => {
    if (!val) {
        for (const key in results) {
            results[key] = null;
        }
        return;
    }
    switch (category) {
        case "all":
            const result_all = await Service.searchApiV1SearchAutocompleteGet(
                val
            );
            for (const key in result_all) {
                results[key] = result_all[key];
            }
            break;
        case "musicians":
            const result_musicians =
                await Service.searchMusicianApiV1SearchMusicianGet(val);
            results.musicians = result_musicians;
            break;
        case "albums":
            const result_albums = await Service.searchAlbumApiV1SearchalbumGet(
                val
            );
            for (const key in results) {
                results[key] = [];
            }
            results.albums = result_albums;
            break;

        case "tracks":
            const result_tracks = await Service.searchTrackApiV1SearchTrackGet(
                val
            );
            for (const key in results) {
                results[key] = [];
            }
            results.tracks = result_tracks;
            break;
    }
});
const onSearchActiveUpdate = (val) => {
    emit("update:searchActive", val);
};
</script>

<style lang="scss">
#search-modal {
    padding-top: 20vh;

    .modal-content {
        width: 100%;
        justify-content: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding: 20px;
        .results-categories {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;

            .back-button {
                display: flex;
                align-items: center;
                gap: 5px;
                padding: 8px 16px;
                border-radius: 5px;
                background-color: $quinary-bg;
                white-space: nowrap;
                cursor: pointer;
                user-select: none;
                &:hover {
                    background-color: $quaternary-bg;
                }
            }

            .current-category {
                gap: 5px;
                padding: 8px 16px;
                border-radius: 5px;
                background-color: $quinary-bg;
                white-space: nowrap;
                user-select: none;
                flex-grow: 1;
                text-align: center;
            }
        }
        .results {
            height: 100%;
            transition: 0.3s ease all;
            display: flex;
            flex-direction: column;
            gap: 10px;
            .results-item-title {
                color: $secondary-text;
                display: flex;
                align-items: center;
                gap: 5px;
                border-radius: 5px;
                width: min-content;
                white-space: nowrap;
                cursor: pointer;
                user-select: none;
                position: relative;
                transition: 0.2s ease all;

                &::after {
                    position: absolute;
                    width: 0%;
                    content: "";
                    bottom: -1px;
                    border-radius: 5px;
                    display: block;
                    height: 1px;
                    background-color: $tertiary-text;
                    transition: 0.2s width;
                }
                &:hover {
                    color: $primary-text;
                    &::after {
                        background-color: $primary-text;
                        width: 100%;
                    }
                }
            }

            .results-item {
                width: 100%;
                display: flex;
                flex-wrap: wrap;
                gap: 10px;

                &.musicians {
                    display: grid;
                    grid-template-columns: repeat(5, 1fr);
                }
            }
        }
        .el-input {
            --el-input-bg-color: #{$quaternary-bg};
            --el-input-border-color: transparent;
            --el-input-hover-border-color: transparent;
            --el-input-focus-border-color: transparent;
            --el-input-height: 60px;
            --el-input-text-color: #{$primary-text};
            .el-input__wrapper {
                font-size: large;
            }
        }
    }
}
</style>
