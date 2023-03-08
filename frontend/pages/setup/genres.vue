<template>
    <SetupContainer class="genres-setup">
        <template #headline>
            Выберите жанры,<br />
            которые вам нравятся
        </template>
        <template #description>
            Это поможет получать более точные и интересные рекомендации
        </template>
        <template #content>
            <AppInput
                v-model="search"
                :placeholder="placeholder"
                class="genres-setup-input"
                size="large"
                :resize-on-focus="false"
                height="50px"
            />
            <div class="genres">
                <GenreCard
                    v-for="genre in genres"
                    :key="genre.id"
                    :genre="genre"
                />
            </div>
        </template>
        <template #button>Далее</template>
    </SetupContainer>
</template>
<script setup>
import { Service } from "~~/client";
definePageMeta({
    layout: "full",
});
const placeholder = ref("Найди свой жанр");
const search = ref("");
const randomGenres = await Service.getRandomGenresApiV1GenresRandomGet();
const typeGenreTimeout = 800;
const typeGenre = (genre) => {
    placeholder.value = "";
    var currentIndex = 0;
    var reverse = false;
    var wait = false;
    setInterval(() => {
        if (!reverse && currentIndex < genre.length) {
            placeholder.value += genre[currentIndex];
            currentIndex++;
        } else {
            wait = true;
            setTimeout(() => {
                reverse = true;
                wait = false;
            }, 1500);
        }
        if (reverse && currentIndex > 0) {
            placeholder.value = placeholder.value.slice(0, -1);
            currentIndex--;
        } else {
            clearInterval();
        }
    }, typeGenreTimeout / genre.length);
};

setTimeout(() => {
    const interval = setInterval(() => {
        if (placeholder.value.length > 0) {
            placeholder.value = placeholder.value.slice(0, -1);
        } else {
            clearInterval(interval);
        }
    }, 100);
    setTimeout(() => {
        typeGenre(randomGenres[0].name);
        setInterval(() => {
            const randomGenre =
                randomGenres[Math.floor(Math.random() * randomGenres.length)];
            typeGenre(randomGenre.name);
        }, typeGenreTimeout * 2 + 1500);
    }, placeholder.value.length * 100 + 1000);
}, 3000);

const popularGenres = await Service.getGenresApiV1GenresGet();
const genres = computed(() => {
    if (!search.value) {
        return popularGenres;
    }

    return [];
});
</script>
<style lang="scss">
.genres-setup {
    .genres {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        grid-auto-rows: min-content;
        gap: 20px;
        width: 100%;
    }
    .genres-setup-input {
        font-size: 1rem;
        margin-bottom: 20px;
    }
}
</style>
