<template>
    <SetupContainer
        class="genres-setup"
        @skip="resultCheck(resultRouteName)"
        :next-button="nextPage"
        :skip-button="!nextPage"
        @next="nextPage && $router.push({ name: resultRouteName })"
        v-model:search="search"
        v-model:modal-active="showWarningModal"
        modal-headline="Вы не выбрали ни одного жанра"
        modal-description="Выберите хотя бы один жанр, чтобы получать более точные рекомендации"
        :modal-buttons="[
            {
                text: 'Вернуться',
                onClick: () => (showWarningModal = false),
            },
            {
                text: 'Далее',
                onClick: () => $router.push({ name: resultRouteName }),
            },
        ]"
        :placeholder="typingText"
    >
        <template #headline>
            Выберите жанры,<br v-if="$viewport.isGreaterOrEquals('lg')" />
            которые вам нравятся
        </template>
        <template #description>
            Это поможет получать более точные и интересные рекомендации
        </template>
        <template #items>
            <SetupGenresCard
                v-for="(genre, index) in genres"
                :genre="genre"
                @liked="(liked) => onLike(liked, index)"
                :key="genre.id"
            />
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
        type: Boolean,
        default: false,
    },
});
const { logined } = storeToRefs(useAuthStore());
const router = useRouter();
if (!logined.value) {
    router.push({ name: routesNames.login });
}

const runtimeConfig = useRuntimeConfig();
const search = ref("");
const randomGenres = await Service.getRandomGenresApiV1GenresRandomGet();
const randomGenresNames = randomGenres.map((genre) => genre.name);
const { typingText } = useTyping(randomGenresNames, "Найди свой жанр");
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
    const currentGenre = genres.value[index];
    var removeArray = liked ? popularGenres : favoriteGenres;
    var addArray = liked ? favoriteGenres : popularGenres;
    removeArray.value = removeArray.value.filter(
        (genre) => genre.id !== currentGenre.id
    );
    addArray.value.push(currentGenre);
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
        showWarningModal.value = true;
        return;
    }
    router.push({ name: routeName });
};
</script>
