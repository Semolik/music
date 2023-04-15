<template>
    <div class="favorite-page-container">
        <Transition name="fade">
            <div
                @click="filtersMenuOpened = false"
                class="bg"
                v-if="filtersMenuOpened"
            ></div>
        </Transition>
        <div class="buttons-line">
            <div
                :class="[
                    'filters',
                    { opened: filtersMenuOpened },
                    { active: filtersIsActived },
                ]"
            >
                <div
                    class="filters-button filter"
                    @click="filtersMenuOpened = !filtersMenuOpened"
                    ref="filtersButton"
                >
                    Фильтры
                </div>
                <div
                    class="filters-button add"
                    @click="createPlaylistModalOpened = true"
                >
                    Создать плейлист
                </div>
                <ModalDialog
                    @close="createPlaylistModalOpened = false"
                    :active="createPlaylistModalOpened"
                >
                    <template #content>
                        <PlaylistCreateModalContent
                            @creared="onCreatedPlaylist"
                        />
                    </template>
                </ModalDialog>
                <div class="filters-menu" ref="filtersMenu">
                    <div
                        class="filter-item"
                        v-for="(filter, name) in filters"
                        :key="filter.title"
                    >
                        <div class="disabled" v-if="filter.disabled">
                            <Icon name="material-symbols:lock" />
                        </div>
                        <div class="title">{{ name }}</div>
                        <div class="values">
                            <div
                                :class="[
                                    'value',
                                    {
                                        active:
                                            filter.active === value ||
                                            (!filter.active &&
                                                filter.default === value),
                                    },
                                ]"
                                v-for="value in filter.values"
                                :key="value"
                                @click="filter.active = value"
                            >
                                {{ value }}
                            </div>
                        </div>
                    </div>
                    <div
                        @click="resetFilters"
                        :class="['reset-button', { active: filtersIsActived }]"
                    >
                        Cбросить фильтры
                    </div>
                </div>
            </div>
        </div>
        <ClientOnly>
            <div class="playlists-contaner" v-auto-animate>
                <PlaylistCard
                    v-for="playlist in playlists"
                    :playlist="playlist"
                    :key="playlist.id"
                    is-link
                />
            </div>
        </ClientOnly>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { IconsNames } from "~~/configs/icons";
const filtersMenuOpened = ref(false);
const filtersMenu = ref(null);
const createPlaylistModalOpened = ref(false);

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
        values: ["По возрастанию", "По убыванию"],
        active: null,
        default: "По возрастанию",
    },
});
const fething = ref(false);
const playlists = ref([]);
const reseting = ref(false);
const getPlaylists = async () => {
    fething.value = true;
    playlists.value = [];
    const order_by =
        filters["Сортировать по"].active === "Названию" ? "name" : "created_at";
    const order =
        filters["Направление сортировки"].active === "По возрастанию"
            ? "asc"
            : "desc";
    const owned_only = filters["Создатель"].active === "Мои" ? true : false;
    const private_ = filters["Тип"].active === "Приватные" ? true : false;
    playlists.value = await Service.getMyPlaylistsApiV1PlaylistsGet(
        order_by,
        order,
        owned_only,
        private_
    );
    fething.value = false;
};
watch(
    filters,
    async (value) => {
        if (reseting.value) return;
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
const filtersIsActived = computed(() => {
    return Object.values(filters).some(
        (filter) => filter.active && filter.active !== filter.default
    );
});
const resetFilters = async (on_reset = false) => {
    reseting.value = true;
    filtersMenuOpened.value = false;
    Object.values(filters).forEach((filter) => {
        filter.active = null;
        filter.disabled = false;
    });

    reseting.value = on_reset;
    await getPlaylists();
};
const onCreatedPlaylist = async (playlist) => {
    createPlaylistModalOpened.value = false;
    await resetFilters();
    playlists.value.unshift(playlist);
};
const filtersButton = ref(null);
onMounted(() => {
    onClickOutside(filtersMenu, (e) => {
        if (e.target === filtersButton.value) return;
        filtersMenuOpened.value = false;
    });
});
</script>
<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.favorite-page-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .bg {
        position: absolute;
        z-index: 90;
        background-color: rgba(0, 0, 0, 0.5);
        transition: opacity 0.3s ease;
        inset: 0;
    }
    .filters {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        position: relative;
        &.active {
            .filters-button {
                &.filter {
                    background-color: $accent;
                    color: $primary-bg;

                    &:hover {
                        background-color: $accent-hover;
                    }
                }
            }
        }

        &.opened .filters-menu {
            opacity: 1;
            z-index: 99;
        }

        @include lg {
            &:not(.opened) {
                .filters-button:hover {
                    background-color: $quaternary-bg;
                }
            }
        }

        .filters-button {
            @include flex-center;
            border-radius: 10px;
            padding: 5px 20px;
            gap: 5px;
            background-color: $tertiary-bg;
            cursor: pointer;
            color: $secondary-text;
            user-select: none;
            &.add {
                margin-left: auto;
            }
            @include lg(true) {
                flex-grow: 1;
            }

            svg {
                width: 20px;
                height: 20px;
            }
        }
        .filters-menu {
            position: absolute;
            top: calc(100% + 10px);
            background-color: $quaternary-bg;
            border-radius: 10px;
            padding: 10px;
            opacity: 0;
            z-index: -1;
            display: flex;
            flex-direction: column;
            gap: 10px;
            border: 1px solid $quaternary-text;
            @include lg(true) {
                width: 100%;
            }
            .reset-button {
                @include flex-center;
                border-radius: 10px;
                cursor: pointer;
                user-select: none;
                padding: 5px 10px;
                height: min-content;
                background-color: $accent-red;
                color: $primary-bg;
                display: none;
                &.active {
                    display: flex;
                }
            }

            .filter-item {
                display: flex;
                flex-direction: column;
                gap: 5px;
                position: relative;
                .disabled {
                    position: absolute;
                    inset: -3px;
                    border-radius: 10px;
                    background-color: rgba(0, 0, 0, 0.5);
                    @include flex-center;

                    svg {
                        width: 30px;
                        height: 30px;
                        color: $secondary-text;
                    }
                }
                .title {
                    font-size: 14px;
                    color: $secondary-text;
                }
                .values {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 5px;
                    padding: 5px;
                    background-color: $tertiary-bg;
                    border-radius: 10px;
                    .value {
                        @include flex-center;
                        height: 30px;
                        border-radius: 5px;
                        cursor: pointer;
                        color: $secondary-text;
                        user-select: none;
                        flex-grow: 1;
                        padding: 0 10px;
                        text-align: center;

                        &.active {
                            background-color: $accent;
                            color: $primary-bg;
                        }
                    }
                }
            }
        }
    }
    .playlists-contaner {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
        gap: 10px;
        @include lg(true) {
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        }
        grid-template-rows: min-content;
    }
}
</style>
