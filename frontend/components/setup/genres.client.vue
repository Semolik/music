<template>
    <SetupContainer
        class="genres-setup"
        @skip="skip"
        :next-button="!!nextPage"
        @next="nextPage && $router.push({ name: nextPage })"
        v-model:search="search"
        :placeholder="placeholder"
        v-model:modal-active="showWarningModal"
        modal-headline="Вы не выбрали ни одного жанра"
        modal-description="Выберите хотя бы один жанр, чтобы получать более точные рекомендации"
        :modal-buttons="[
            {
                text: 'Вернуться',
                onClick: () => (showWarningModal = false),
            },
            {
                text: 'Пропустить',
                onClick: () => $router.push({ name: resultRouteName }),
            },
        ]"
    >
        <template #headline>
            Выберите жанры,<br v-if="$viewport.isGreaterOrEquals('lg')" />
            которые вам нравятся
        </template>
        <template #description>
            Это поможет получать более точные и интересные рекомендации
        </template>
        <template #content>
            <div class="genres" v-auto-animate>
                <GenreCard
                    v-for="(genre, index) in genres"
                    :genre="genre"
                    @liked="(liked) => onLike(liked, index)"
                    overlay-on-like
                />
            </div>
        </template>
    </SetupContainer>
</template>
<script setup>
import { Service } from "~~/client";
import { FilterGenreEnum } from "~~/client/models/FilterGenreEnum";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames } from "~~/.nuxt/typed-router";
const { resultRouteName, nextPage } = defineProps({
    resultRouteName: {
        type: String,
        default: routesNames.settings.profile,
    },
    nextPage: {
        type: String,
    },
});
const { logined } = storeToRefs(useAuthStore());
const router = useRouter();
if (!logined.value) {
    router.push({ name: routesNames.login });
}

const runtimeConfig = useRuntimeConfig();
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

const popularGenres = ref(
    await Service.getGenresApiV1GenresGet(
        1,
        runtimeConfig.public.SEARCH_GENRE_LIMIT,
        FilterGenreEnum.NOT_LIKED
    )
);
const favoriteGenres = ref(
    await Service.getGenresApiV1GenresGet(
        1,
        runtimeConfig.public.SEARCH_GENRE_LIMIT,
        FilterGenreEnum.LIKED
    )
);

const mergedGenres = [...favoriteGenres.value, ...popularGenres.value];
const genres = ref(mergedGenres);
const onLike = (liked, index) => {
    genres.value[index].liked = liked;
    if (liked) {
        favoriteGenres.value.push(genres.value[index]);
        popularGenres.value = popularGenres.value.filter(
            (genre) => genre.id !== genres.value[index].id
        );
    } else {
        favoriteGenres.value = favoriteGenres.value.filter(
            (genre) => genre.id !== genres.value[index].id
        );
        popularGenres.value.push(genres.value[index]);
    }
};
watch(
    search,
    async (value) => {
        if (!value) {
            genres.value = [...favoriteGenres.value, ...popularGenres.value];
            return;
        }
        genres.value = await Service.getGenresApiV1SearchGenresGet(value);
    },
    { immediate: true }
);
const showWarningModal = ref(false);
const resultCheck = async (routeName) => {
    var currentLikedGenres = await Service.getGenresApiV1GenresGet(
        1,
        runtimeConfig.public.SEARCH_GENRE_LIMIT,
        FilterGenreEnum.LIKED
    );

    if (currentLikedGenres.length === 0) {
        console.log("show modal");
        showWarningModal.value = true;
        return;
    }
    router.push({ name: routeName });
};
const skip = async () => {
    resultCheck(resultRouteName);
};
</script>
<style lang="scss" scoped>
.genres-setup {
    .genres {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        grid-auto-rows: min-content;
        gap: 20px;
        width: 100%;
    }
}
</style>
