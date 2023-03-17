<template>
    <div class="genres" ref="genresContainer">
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
</template>
<script setup>
import { Service } from "@/client";
import { IconsNames } from "~~/configs/icons";
definePageMeta({
    middleware: ["admin"],
});
const genresContainer = ref(null);
const getGenres = async (page) => {
    return await Service.getGenresApiV1GenresGet(page);
};
const page = ref(1);
const genres = ref(await getGenres(page.value));
const disabled = ref(false);
onMounted(() => {
    useInfiniteScroll(
        genresContainer,
        async () => {
            if (disabled.value) {
                return;
            }
            page.value++;
            const items = await getGenres(page.value);
            if (items.length === 0) {
                disabled.value = true;
            }
            genres.value.push(...items);
        },
        { distance: 10 }
    );
});
</script>
<style scoped lang="scss">
.genres {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 5px;

    overflow: auto;
    padding-right: 5px;
    @include lg(true) {
        height: 82cqh;
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
</style>
