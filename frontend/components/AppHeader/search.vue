<template>
    <ModalDialog
        :active="props.searchActive"
        @update:active="onSearchActiveUpdate"
        :padding="20"
        id="search-modal"
        :max-width="800"
        :max-height="600"
        off-justify-content
    >
        <template #header>
            <span class="font-medium mb-2">
                Поиск по трекам, альбомам, клипам, исполнителям и плейлистам
            </span>
        </template>
        <template #content>
            <el-input
                placeholder="Введите запрос"
                v-model="searchQuery"
                size="large"
            />
            <div :class="['results-categories', { disabled: !searchQuery }]">
                <div
                    :class="[
                        'results-categories-item',
                        { active: category === 'all' },
                    ]"
                    @click="category = 'all'"
                >
                    Все результаты
                </div>
                <div
                    :class="[
                        'results-categories-item',
                        { active: category === 'tracks' },
                    ]"
                    @click="category = 'tracks'"
                >
                    Треки
                </div>
                <div
                    :class="[
                        'results-categories-item',
                        { active: category === 'albums' },
                    ]"
                    @click="category = 'albums'"
                >
                    Альбомы
                </div>
                <div
                    :class="[
                        'results-categories-item',
                        { active: category === 'artists' },
                    ]"
                    @click="category = 'artists'"
                >
                    Исполнители
                </div>
                <div
                    :class="[
                        'results-categories-item',
                        { active: category === 'playlists' },
                    ]"
                    @click="category = 'playlists'"
                >
                    Плейлисты
                </div>
            </div>
            <div class="results">{{ results[category] }}</div>
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
const results = reactive({
    all: null,
    albums: null,
    artists: null,
    playlists: null,
    tracks: null,
});
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
            results.all = result_all;
            break;
        case "artists":
            const result_musicians =
                await Service.searchMusicianApiV1SearchMusicianGet(val);
            results.artists = result_musicians;
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
        .results-categories {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;

            .results-categories-item {
                padding: 8px 16px;
                border-radius: 5px;
                background-color: $quaternary-bg;
                white-space: nowrap;
                opacity: 0.5;
                cursor: pointer;
                user-select: none;
                &.active {
                    opacity: 1;
                }
            }
        }
        .results {
            overflow: auto;
            height: 100%;
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
