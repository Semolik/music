<template>
    <div class="genres-page-container">
        <AddSearch
            :to="{ name: routesNames.adminCabinet.cabinetGenresNew }"
            v-model:search="search"
            placeholder="Поиск по жанрам"
        />
        <ClientOnly>
            <div class="genres" ref="genresContainer" v-auto-animate>
                <nuxt-link
                    class="genre"
                    v-for="genre in genres"
                    :key="genre.id"
                    :to="{
                        name: routesNames.adminCabinet.cabinetGenresId,
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

        <AppButton
            class="show-more-button"
            :disabled="disabled"
            @click="showMore"
            v-if="showMoreButton"
        >
            Показать еще
        </AppButton>
    </div>
</template>
<script setup>
import { Service } from "@/client";
import { IconsNames } from "~~/configs/icons";
import { routesNames } from "@typed-router";
definePageMeta({
    middleware: ["admin"],
});
useHead({ title: "Жанры" });
const runtimeConfig = useRuntimeConfig();
const genresContainer = ref(null);
const getGenres = async (page) => {
    return await Service.getGenresApiV1GenresGet(page);
};
const page = ref(1);
const genres = ref(await getGenres(page.value));
const disabled = ref(false);
const showMoreButton = ref(
    genres.length === runtimeConfig.public.SEARCH_GENRE_LIMIT
);
const showMore = async () => {
    page.value++;
    const newGenres = await getGenres(page.value);
    if (newGenres.length === 0) {
        showMoreButton.value = false;
        return;
    }
    genres.value = [...genres.value, ...newGenres];
};
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
