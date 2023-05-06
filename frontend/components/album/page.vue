<template>
    <SettingsPage :title="title" max-width="100%" padding="0px">
        <div class="album-page">
            <Upload
                border-radius="10px"
                :imageUrl="picture"
                class="genre-image-uploader"
                name="genrePicture"
                @file="handleAvatarSuccess"
                :icon="IconsNames.imageIcon"
            />
            <div class="fields">
                <div class="items">
                    <AppInput
                        v-model="name"
                        label="Название"
                        :error="!name"
                        :max-length="MAX_ALBUM_NAME_LENGTH"
                        show-word-limit
                    />
                    <div class="app-input">
                        <label class="app-input__label">
                            Дата выхода альбома
                        </label>
                        <el-date-picker
                            v-model="openDate"
                            type="datetime"
                            placeholder="Дата открытия"
                            id="date-picker"
                        />
                    </div>
                </div>
                <GenresSelector v-model="genres" class="genres-selector" />
                <div class="items">
                    <template v-if="id">
                        <AppButton
                            v-if="!album.uploaded"
                            @click="goToEditTracks(album)"
                            active
                        >
                            Редактировать треки
                        </AppButton>
                        <AppButton
                            v-else
                            @click="goToAlbum(album)"
                            :active="albumIsOpened"
                        >
                            Перейти к альбому
                        </AppButton>
                    </template>

                    <AppButton
                        :active="buttonIsActive"
                        @click="id ? updateAlbum() : createAlbum()"
                    >
                        {{
                            id
                                ? "Обновить"
                                : "Создать и перейти к загрузке треков"
                        }}
                    </AppButton>
                </div>
                <AppButton
                    v-if="id"
                    @click="deleteModalOpened = true"
                    active
                    class="delete"
                >
                    Удалить альбом
                </AppButton>
                <ModalDialog
                    :active="deleteModalOpened"
                    @close="deleteModalOpened = false"
                    head-text="Удаление альбома"
                    :buttons="[
                        {
                            text: 'Удалить',
                            onClick: deleteAlbum,
                            active: true,
                            red: true,
                        },
                        {
                            text: 'Отмена',
                            onClick: () => (deleteModalOpened = false),
                        },
                    ]"
                >
                    <template #content>
                        Вы уверены, что хотите удалить альбом? <br />
                        Это действие нельзя будет отменить. <br />
                        Все треки, входящие в альбом, также будут удалены.
                    </template>
                </ModalDialog>
            </div>
        </div>
    </SettingsPage>
</template>
<script setup>
import { Service } from "~/client";
import { useToast } from "vue-toastification";
import { IconsNames } from "~/configs/icons";
import { routesNames } from "~/.nuxt/typed-router";
import moment from "moment";
const { id } = defineProps({
    id: {
        type: String,
        required: false,
        default: null,
    },
});
const toast = useToast();
const { MAX_ALBUM_NAME_LENGTH } = useRuntimeConfig().public;

const album = id
    ? ref(await Service.getAlbumInfoByIdApiV1AlbumsAlbumIdInfoGet(id))
    : {};

const title = computed(() =>
    id ? "Редактирование альбома " + album.value.name : "Создание альбома"
);
useHead({
    title: title.value,
});
const deleteModalOpened = ref(false);
const picture = ref(album.value?.picture || null);
const pictureBlob = ref(null);
const handleAvatarSuccess = (raw) => {
    pictureBlob.value = raw;
    picture.value = URL.createObjectURL(raw);
};
const genres = ref(id ? album.value.genres : []);
const name = ref(id ? album.value.name : "");
const genresIsChanged = computed(() => {
    if (genres.value.length !== album.value.genres.length) {
        return true;
    }
    return genres.value.some((g) => !album.value.genres.includes(g));
});
const openDate = ref(id ? moment(album.value.open_date).toDate() : new Date());
const buttonIsActive = computed(() => {
    if (!id) {
        return !!(
            name.value.length > 0 &&
            genres.value.length > 0 &&
            pictureBlob.value
        );
    }

    return !!(
        name.value !== album.value.name ||
        pictureBlob.value ||
        genresIsChanged.value ||
        moment(album.value.open_date).toDate().toDateString() !==
            openDate.value.toDateString()
    );
});

const router = useRouter();
const goToEditTracks = (album) => {
    router.push({
        name: routesNames.musicianCabinet.cabinetAlbumsIdTracks,
        params: { id: album.id },
    });
};
const now = new Date();
const albumIsOpened = computed(
    () => moment(album.value.open_date).toDate() < now
);
const goToAlbum = (album) => {
    if (!albumIsOpened.value) {
        toast.error("Альбом еще не открыт");
        return;
    }
    router.push({
        name: routesNames.albumId,
        params: { id: album.id },
    });
};
const createAlbum = async () => {
    if (!buttonIsActive.value) {
        return;
    }
    try {
        const new_album = await Service.createAlbumApiV1AlbumsPost({
            albumData: JSON.stringify({
                name: name.value,
                genres_ids: genres.value.map((g) => g.id),
                open_date: openDate.value,
            }),
            albumPicture: pictureBlob.value,
        });
        goToEditTracks(new_album);
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    }
};
const updateAlbum = async () => {
    if (!buttonIsActive.value) {
        return;
    }
    try {
        const updated_album = await Service.updateAlbumApiV1AlbumsAlbumIdPut(
            id,
            {
                albumData: JSON.stringify({
                    name: name.value,
                    genres_ids: genres.value.map((g) => g.id),
                    open_date: openDate.value,
                }),
                albumPicture: pictureBlob.value,
            }
        );
        album.value = updated_album;
        genres.value = updated_album.genres;
        pictureBlob.value = null;
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    }
};
const deleteAlbum = async () => {
    try {
        await Service.deleteAlbumByIdApiV1AlbumsAlbumIdDelete(id);
        router.push({
            name: routesNames.musicianCabinet.cabinetAlbums,
        });
    } catch (e) {
        toast.error(HandleOpenApiError(e).message);
    }
};
</script>

<style lang="scss">
@import url(element-plus/theme-chalk/dark/css-vars.css);
.el-date-editor {
    --el-input-border-radius: 10px;
    --el-date-editor-width: 100%;
    --app-input-height: 100%;
    --el-input-height: 40px;
    .el-input__wrapper {
        --el-input-height: 40px;
        width: 100%;
    }
}
.genres-selector {
    margin-top: 5px;
}
.album-page {
    display: grid;
    grid-template-columns: 230px 1fr;
    gap: 10px;

    @include lg(true) {
        grid-template-columns: 1fr;
    }
    .fields {
        display: flex;
        gap: 10px;
        flex-direction: column;
        .items {
            display: flex;
            gap: 10px;
            @include lg(true) {
                flex-direction: column;
            }
        }
        .delete {
            --app-button-active-bg: #{$accent-red};
            --app-button-active-hover-bg: #{$accent-red-hover};
        }
    }
}
</style>
