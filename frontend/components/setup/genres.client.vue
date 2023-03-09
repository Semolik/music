<template>
    <SetupContainer class="genres-setup" @skip="skip" :next-button="false">
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
            <div class="genres" v-auto-animate>
                <GenreCard
                    v-for="(genre, index) in genres"
                    :key="genre.id"
                    :genre="genre"
                    @liked="(event) => (genres[index].liked = event)"
                    :force-overlay="genres[index].liked"
                />
            </div>
        </template>
    </SetupContainer>
    <ModalDialog
        v-model:active="showWarningModal"
        @close="showWarningModal = false"
    >
        <template #content>
            <div class="warning-modal">
                <div class="warning-modal-headline">
                    Вы не выбрали ни одного жанра
                </div>
                <div class="warning-modal-description">
                    Выберите хотя бы один жанр, чтобы получать более точные
                    рекомендации
                </div>
                <div class="warning-modal-buttons">
                    <div class="button" @click="showWarningModal = false">
                        Отмена
                    </div>
                    <div
                        class="button"
                        @click="$router.push({ name: resultRouteName })"
                    >
                        Ок
                    </div>
                </div>
            </div>
        </template>
    </ModalDialog>
</template>
<script setup>
import { Service } from "~~/client";
import { FilterGenreEnum } from "~~/client/models/FilterGenreEnum";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { routesNames } from "~~/.nuxt/typed-router";
const { resultRouteName } = defineProps({
    resultRouteName: {
        type: String,
        default: routesNames.settings.profile,
    },
});
const { logined } = storeToRefs(useAuthStore());
const router = useRouter();
if (!logined.value) {
    router.push(routesNames.login);
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

const popularGenres = await Service.getGenresApiV1GenresGet(
    1,
    runtimeConfig.public.SEARCH_GENRE_LIMIT,
    FilterGenreEnum.NOT_LIKED
);

const favoriteGenres = await Service.getGenresApiV1GenresGet(
    1,
    runtimeConfig.public.SEARCH_GENRE_LIMIT,
    FilterGenreEnum.LIKED
);
const mergedGenres = [...favoriteGenres, ...popularGenres];
const genres = ref(mergedGenres);
watch(
    search,
    async (value) => {
        if (!value) {
            genres.value = mergedGenres;
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
    console.log(currentLikedGenres);
    if (currentLikedGenres.length === 0) {
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
.warning-modal {
    padding: 20px;
    display: flex;
    gap: 10px;
    flex-direction: column;
    .warning-modal-headline {
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
    }
    .warning-modal-description {
        font-size: 1rem;
        font-weight: 400;
    }
    .warning-modal-buttons {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;

        .button {
            padding: 10px;
            border-radius: 10px;
            background-color: $quaternary-bg;
            font-weight: 600;
            flex-grow: 1;
            cursor: pointer;
            text-align: center;

            &:hover {
                background-color: $quinary-bg;
            }
        }
    }
}
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
