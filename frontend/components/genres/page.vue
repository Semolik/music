<template>
    <SettingsPage :title="title" max-width="100%" padding="0" v-if="!loading">
        <form class="content" ref="form" @submit.prevent="updateGenre">
            <Upload
                :imageUrl="picture"
                class="avatar-uploader"
                name="genrePicture"
                border-radius="5px"
                @file="handleAvatarSuccess"
                :icon="IconsNames.imageIcon"
            />
            <div class="right">
                <AppInput
                    label="Название жанра"
                    :max-length="MAX_GENRE_NAME_LENGTH"
                    :min-length="1"
                    v-model="name"
                    show-word-limit
                    class="name-input"
                />
                <div class="genre-info" v-if="id">
                    <div class="info-card">
                        <Icon :name="IconsNames.likeIcon" />
                        <div class="info-card-text">
                            <div class="info-card-text-headline">
                                Количество лайков
                            </div>
                            <div class="info-card-text-value">
                                {{ genre.likes }}
                            </div>
                        </div>
                    </div>
                    <div class="info-card">
                        <Icon :name="IconsNames.albumIcon" />
                        <div class="info-card-text">
                            <div class="info-card-text-headline">
                                Количество альбомов
                            </div>
                            <div class="info-card-text-value">
                                {{ genre.album_count }}
                            </div>
                        </div>
                    </div>
                </div>
                <div class="buttons">
                    <AppButton
                        border-radius="5px"
                        class="remove-button"
                        active
                        @click="showDeleteDialog = true"
                        v-if="id"
                    >
                        Удалить
                    </AppButton>
                    <AppButton
                        :active="buttonActive"
                        @click="
                            (event) =>
                                id ? updateGenre(event) : createGenre(event)
                        "
                        border-radius="5px"
                    >
                        {{ id ? "Сохранить" : "Создать" }}
                    </AppButton>
                </div>
            </div>
        </form>
        <ModalDialog
            :active="showDeleteDialog"
            @close="showDeleteDialog = false"
            :buttons="[
                {
                    text: 'Удалить',
                    type: 'danger',
                    onClick: deleteGenre,
                },
                {
                    text: 'Отмена',
                    type: 'primary',
                    onClick: () => {
                        showDeleteDialog = false;
                    },
                },
            ]"
        >
            <template #content>
                Вы уверены, что хотите удалить жанр {{ genre.name }}?
            </template>
        </ModalDialog>
    </SettingsPage>
</template>
<script setup>
import { Service } from "@/client";
import { routesNames } from "@typed-router";
import { IconsNames } from "~~/configs/icons";
import { useToast } from "vue-toastification";

const { id } = defineProps({
    id: {
        type: String,
        default: null,
    },
});
const toast = useToast();
const runtimeConfig = useRuntimeConfig();
const { MAX_GENRE_NAME_LENGTH } = runtimeConfig.public;
const router = useRouter();

const genre = ref({});
const loading = ref(true);
const getGenre = async (id) => {
    try {
        return await Service.getGenreInfoApiV1GenresGenreIdGet(id);
    } catch (e) {
        router.push({ name: routesNames.adminCabinet.cabinetGenres });
    }
};
const picture = ref("");
const pictureBlob = ref(null);
const handleAvatarSuccess = (raw) => {
    pictureBlob.value = raw;
    picture.value = URL.createObjectURL(raw);
};
const deleteGenre = async () => {
    try {
        await Service.deleteGenreApiV1GenresGenreIdDelete(id);
        router.push({ name: routesNames.adminCabinet.cabinetGenres });
    } catch (e) {
        toast.error("Не удалось удалить жанр");
    }
};
const form = ref(null);
const name = ref("");
const title = computed(() =>
    id ? `Редактирование жанра ${genre.value.name}` : `Создание жанра`
);
useHead({ title: title });
const buttonActive = computed(() => {
    return (
        name.value.length >= 1 &&
        (id
            ? name.value !== genre.value.name ||
              picture.value !== genre.value.picture
            : pictureBlob.value !== null)
    );
});
const showDeleteDialog = ref(false);
const updateGenre = async () => {
    if (!buttonActive.value) return;

    try {
        const genreData = await Service.updateGenreApiV1GenresGenreIdPut(id, {
            name: name.value,
            genrePicture: pictureBlob.value,
        });
        genre.value = genreData;
        picture.value = genreData.picture;
        pictureBlob.value = null;
    } catch (e) {
        toast.error("Не удалось обновить жанр");
    }
};
const createGenre = async () => {
    if (!buttonActive.value) return;

    try {
        const genreData = await Service.createGenreApiV1GenresPost({
            name: name.value,
            genrePicture: pictureBlob.value,
        });
        router.push({
            name: routesNames.adminCabinet.cabinetGenresId,
            params: { id: genreData.id },
        });
    } catch (e) {
        toast.error("Не удалось создать жанр");
    }
};
onMounted(async () => {
    if (!id) {
        loading.value = false;
        return;
    }
    genre.value = await getGenre(id);
    name.value = genre.value.name;
    picture.value = genre.value.picture;
    loading.value = false;
});
</script>
<style lang="scss" scoped>
.content {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 5px;
    @include xl(true) {
        @include flex-center;
        flex-direction: column;
    }
    .avatar-uploader {
        width: 100%;
        height: 100%;
        max-width: 450px;
    }
    .right {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 5px;
        .name-input {
            --app-input-border-radius: 5px;
        }
        .genre-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
            gap: 5px;
            flex-grow: 1;
            .info-card {
                gap: 5px;
                @include flex-center;
                background-color: $quaternary-bg;
                padding: 10px;
                flex-grow: 1;

                border-radius: 5px;
                color: $secondary-text;
                svg {
                    width: 30px;
                    height: 30px;
                }
                .info-card-text {
                    flex-direction: column;
                    padding-inline: 20px;
                    width: 100%;
                    @include flex-center;
                    .info-card-text-value {
                        font-size: 20px;
                        color: $accent;
                    }
                }
            }
        }
        .buttons {
            display: flex;
            gap: 5px;

            .remove-button {
                --app-button-active-bg: #{$accent-red};
                --app-button-active-hover-bg: #{$accent-red-hover};
            }
        }
    }
}
</style>
