<template>
    <div class="favorite-page-container">
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
                >
                    <div class="text">Фильтры</div>
                    <Icon :name="IconsNames.filter" />
                </div>
                <div class="filters-button add">
                    <div class="text">Создать плейлист</div>
                    <Icon :name="IconsNames.plusIcon" />
                </div>
                <div class="bg" @click="filtersMenuOpened = false"></div>
                <div class="filters-menu" ref="filtersMenu">
                    <div
                        class="filter-item"
                        v-for="(filter, name) in filters"
                        :key="filter.title"
                    >
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
var filters = reactive({
    "Сортировать по": {
        values: ["Названию", "Дате добавления"],
        active: null,
        default: "Названию",
    },
    Тип: {
        values: ["Публичные", "Приватные"],
        active: null,
        default: "Публичные",
    },
    Создатель: {
        values: ["Все", "Мои"],
        active: null,
        default: "Все",
    },
    "Направление сортировки": {
        values: ["По возрастанию", "По убыванию"],
        active: null,
        default: "По возрастанию",
    },
});

const playlists = ref([]);
watch(
    filters,
    async () => {
        playlists.value = [];
        const order_by =
            filters["Сортировать по"].active === "Названию"
                ? "name"
                : "created_at";
        const order =
            filters["Направление сортировки"].active === "По возрастанию"
                ? "asc"
                : "desc";
        playlists.value = await Service.getMyPlaylistsApiV1PlaylistsGet(
            order_by,
            order
        );
    },
    { immediate: true }
);
const filtersIsActived = computed(() => {
    return Object.values(filters).some((filter) => filter.active);
});
const resetFilters = () => {
    filtersMenuOpened.value = false;
    Object.values(filters).forEach((filter) => {
        filter.active = null;
    });
};
onMounted(() => {
    onClickOutside(filtersMenu, () => {
        filtersMenuOpened.value = false;
    });
});
</script>
<style lang="scss" scoped>
.favorite-page-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .filters {
        display: flex;
        gap: 10px;
        position: relative;
        &.active {
            .filters-button {
                &.filter {
                    background-color: $accent;
                    color: $primary-bg;
                }
            }
            @include lg(true) {
                .bg {
                    display: block;
                }
            }
        }
        @include lg(true) {
            .bg {
                display: none;
                position: absolute;
                inset: 0;
                z-index: 90;
            }
        }
        &.opened {
            .filters-button.filter {
                border-color: $accent;
            }
            .filters-menu {
                opacity: 1;
                z-index: 99;
            }
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
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background-color: $tertiary-bg;
            cursor: pointer;
            color: $secondary-text;
            user-select: none;
            border: 1px solid transparent;
            &.add {
                margin-left: auto;
            }
            .text {
                display: none;
            }
            @include lg(true) {
                width: 100%;
                gap: 5px;
                height: min-content;
                padding: 10px;
                .text {
                    display: block;
                }
            }

            svg {
                width: 20px;
                height: 20px;
            }
        }
        .filters-menu {
            position: absolute;
            top: 110%;
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
                height: 0px;
                opacity: 0;
                padding: 0;
                &.active {
                    padding: 10px;
                    height: min-content;
                    opacity: 1;
                    background-color: $accent-red;
                    color: $primary-bg;
                }
            }

            .filter-item {
                display: flex;
                flex-direction: column;
                gap: 5px;
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
