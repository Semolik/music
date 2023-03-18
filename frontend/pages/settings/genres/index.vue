<template>
    <div class="genres-page-container">
        <div class="search-container">
            <AppInput
                class="search"
                placeholder="Поиск по жанрам"
                v-model="search"
                clearable
            />
            <nuxt-link class="add" to="/settings/genres/new">
                <Icon :name="IconsNames.plusIcon" />
            </nuxt-link>
        </div>
        <ClientOnly>
            <div class="genres" ref="genresContainer" v-auto-animate>
                <nuxt-link
                    class="genre"
                    v-for="genre in genres"
                    :key="genre.id"
                    :to="{
                        name: 'settings-genres-id',
                        params: { id: genre.id },
                    }"
                >
                    <div class="picture">
                        <img :src="genre.picture" alt="genre picture" />
                    </div>
                    <div class="name">{{ genre.name }}</div>
                    <div class="likes">
                        <Icon :name="IconsNames.likeIcon" />
                        <span>{{ genre.likes }}</span>
                    </div>
                </nuxt-link>
            </div>
            <div class="empty" v-if="genres.length === 0">
                Ничего не найдено
            </div>
        </ClientOnly>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { IconsNames } from "~~/configs/icons";
definePageMeta({
    middleware: ["admin"],
});
useHead({ title: "Жанры" });
const genresContainer = ref(null);
const getGenres = async (page) => {
    return await Service.getGenresApiV1GenresGet(page);
};
const page = ref(1);
const genres = ref(await getGenres(page.value));
const disabled = ref(false);

const search = ref("");
watch(search, async (value) => {
    page.value = 1;
    if (value.length === 0) {
        disabled.value = true;
        genres.value = await getGenres(page.value);
        return;
    }
    genres.value = await Service.getGenresApiV1SearchGenresGet(value);
    disabled.value = false;
});
</script>
<style scoped lang="scss">
.genres-page-container {
    display: flex;
    flex-direction: column;
    gap: 5px;
    height: 100%;
    .search-container {
        display: grid;
        grid-template-columns: 1fr min-content;
        gap: 5px;
        .search {
            --app-input-border-radius: 5px;
        }
        .add {
            border: 1px solid $quaternary-text;
            width: 40px;
            height: 100%;
            border-radius: 5px;
            @include flex-center;
            background-color: $secondary-bg;

            &:hover {
                border-color: $tertiary-text;
            }
        }
    }

    .empty {
        @include flex-center;
        height: 100%;

        color: $secondary-text;
    }
    .genres {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 5px;
        overflow: hidden;

        @include lg {
            max-height: 600px;
        }
        .genre {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            padding: 5px;
            border-radius: 5px;
            cursor: pointer;
            background-color: $quaternary-bg;
            height: min-content;

            &:hover {
                background-color: $quinary-bg;
            }

            .picture {
                width: 60px;
                height: 60px;
                border-radius: 5px;
                overflow: hidden;
                img {
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                }
            }

            .likes {
                display: flex;
                align-items: center;
                gap: 5px;
                padding-right: 10px;
                color: $secondary-text;
            }
        }
    }
}
</style>
