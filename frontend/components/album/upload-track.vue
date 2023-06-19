<template>
    <div class="upload-track">
        <div class="line">
            <TrackCard
                :track="track"
                min
                create-track-mode
                @edit="toggleEdit"
                class="track-card"
                @delete="OpenDeleteTrackModal"
                :musican-info="musicianInfo"
            />
            <ModalDialog
                :active="deleteTrackModalOpened"
                @close="deleteTrackModalOpened = false"
                head-text="Удаление трека"
                closeOnEsckey
                :buttons="[
                    {
                        text: 'Удалить',
                        onClick: deleteTrack,
                        active: true,
                        red: true,
                    },
                    {
                        text: 'Отмена',
                        onClick: () => (deleteTrackModalOpened = false),
                    },
                ]"
            >
                <template #content>
                    <div class="text-center">
                        Вы уверены, что хотите удалить трек? <br />
                        Это действие нельзя будет отменить.
                    </div>
                </template>
            </ModalDialog>
        </div>
        <div class="edit" v-if="editOpened">
            <div class="info-container">
                <Upload
                    border-radius="10px"
                    :imageUrl="track.picture"
                    class="genre-image-uploader"
                    name="trackPicture"
                    @file="handleSelectSuccess"
                    :icon="IconsNames.imageIcon"
                />

                <div class="fields">
                    <AppInput
                        v-model="track.name"
                        label="Название"
                        :max-length="MAX_TRACK_NAME_LENGTH"
                        :min-length="MIN_TRACK_NAME_LENGTH"
                        show-word-limit
                        :error="nameError"
                    />
                    <AppInput
                        v-model="track.feat"
                        label="Создан при участии"
                        :max-length="MAX_TRACK_FEAT_LENGTH"
                        show-word-limit
                    />
                    <AppButton
                        class="upload"
                        :active="buttonActive"
                        :loading="uploading"
                        @click="props.track.id ? updateTrack() : createTrack()"
                    >
                        {{ props.track.id ? "Обновить" : "Загрузить" }}
                    </AppButton>
                </div>
            </div>
            <UploadFile
                @file="track_file = $event"
                ref="fileUploader"
                :file-size="MAX_TRACK_FILE_SIZE_MB"
                :file-types="['audio/mpeg', 'audio/mp3', 'audio/flac']"
            />
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "~/configs/icons";
import { Service } from "~/client";
const {
    MAX_TRACK_NAME_LENGTH,
    MIN_TRACK_NAME_LENGTH,
    MAX_TRACK_FEAT_LENGTH,
    MAX_TRACK_FILE_SIZE_MB,
} = useRuntimeConfig().public;
const emit = defineEmits(["position-up", "position-down", "update", "delete"]);
const props = defineProps({
    track: {
        type: Object,
        required: true,
    },
    albumId: {
        type: Number,
        required: true,
    },
    musicianInfo: {
        type: Object,
        required: false,
    },
});

const deleteTrackModalOpened = ref(false);

const uploading = ref(false);
const track_file = ref(null);
const blobPicture = ref(null);
const track = reactive({
    ...props.track,
    feat: props.track.feat || "",
});

const OpenDeleteTrackModal = () => {
    if (!props.track.id) {
        emit("delete");
        return;
    }
    deleteTrackModalOpened.value = true;
};
const handleSelectSuccess = (file) => {
    track.picture = URL.createObjectURL(file);
    blobPicture.value = file;
};
const fileUploader = ref(null);
const nameError = computed(
    () =>
        track.name.length < MIN_TRACK_NAME_LENGTH &&
        track.name.length <= MAX_TRACK_NAME_LENGTH
);
const featError = computed(() =>
    track.feat ? track.feat.length > MAX_TRACK_FEAT_LENGTH : false
);
const buttonActive = computed(
    () =>
        !nameError.value &&
        !featError.value &&
        (!props.track?.id
            ? !!track_file.value
            : track.name !== props.track.name ||
              track.feat !== (props.track.feat || "") ||
              !!track_file.value ||
              !!blobPicture.value)
);

const editOpened = ref(!props.track.id);
const toggleEdit = () => {
    if (!props.track.id || (editOpened.value && buttonActive.value)) return;
    editOpened.value = !editOpened.value;
};

const createTrack = async () => {
    if (!buttonActive.value) return;
    if (uploading.value) return;
    uploading.value = true;
    const new_track = await Service.uploadTrackApiV1AlbumsAlbumIdTrackPost(
        props.albumId,
        {
            trackPicture: blobPicture.value,
            track: track_file.value,
            name: track.name,
            feat: track.feat,
        }
    );
    uploading.value = false;
    emit("update", new_track);
    blobPicture.value = null;
    track_file.value = null;
};

const updateTrack = async () => {
    if (!buttonActive.value) return;
    if (uploading.value) return;
    uploading.value = true;
    const updated_track = await Service.updateTrackByIdApiV1TracksTrackIdPut(
        props.track.id,
        {
            trackPicture: blobPicture.value,
            track: track_file.value,
            name: track.name,
            feat: track.feat,
        }
    );
    uploading.value = false;
    emit("update", updated_track);
    blobPicture.value = null;
    track_file.value = null;
};

const deleteTrack = async () => {
    if (uploading.value) return;
    uploading.value = true;
    await Service.deleteTrackApiV1TracksTrackIdDelete(track.id);
    uploading.value = false;
    emit("delete");
};
</script>
<style scoped lang="scss">
.upload-track {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .line {
        display: grid;
        grid-template-columns: 1fr;
        gap: 10px;
        width: 100%;

        .track-card {
            width: 100%;
        }

        .arrows {
            display: flex;
            flex-direction: column;
            padding: 3px 0px;
            justify-content: space-between;
            align-items: center;
            user-select: none;

            .arrow {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background-color: $primary-bg;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                transition: all 0.3s ease;

                &:hover {
                    background-color: $secondary-bg;
                }
            }
        }
    }
    .edit {
        padding: 10px;
        border-radius: 10px;
        background-color: $quaternary-bg;
        display: flex;
        flex-direction: column;
        gap: 10px;
        .info-container {
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 5px;

            @include lg(true) {
                grid-template-columns: 1fr;
            }

            .fields {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                gap: 10px;
                .upload {
                    --app-button-bg: #{$quinary-bg};
                }
            }
        }
    }
}
</style>
