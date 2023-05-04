<template>
    <SettingsPage :title="title" max-width="100%" padding="0">
        <div class="edit-clip-page">
            <div class="clip-picture">
                <Upload
                    border-radius="10px"
                    :icon="IconsNames.imageIcon"
                    aspect-ratio="16/9"
                    :image-url="new_image_url"
                    v-if="image_type === 'Файл'"
                    @file="set_file"
                />

                <div
                    v-else
                    :class="[
                        'clip-picture-image-preview',
                        { error: !image_url_correct || !image_url },
                    ]"
                >
                    <img
                        :src="image_url"
                        @click="show_click_image_error"
                        v-if="image_url && image_url_correct"
                    />
                    <div class="icon" v-else>
                        <Icon :name="IconsNames.imageIcon" />
                    </div>
                </div>

                <AppSelect
                    :values="['Файл', 'Из видео']"
                    v-model="image_type"
                    title="Источник изображения"
                />
            </div>
            <div class="fields">
                <AppInput
                    v-model="name"
                    label="Название"
                    :error="!name"
                    :max-length="MAX_CLIP_NAME_LENGTH"
                    show-word-limit
                />
                <AppInput
                    v-model="url"
                    label="Ссылка на видео"
                    :error="!urlCorrect"
                />
                <TrackCard
                    min
                    :track="clip.track"
                    create-track-mode
                    v-if="clip.track"
                />
                <AppButton
                    active
                    @click="connectToTrackModalOpened = true"
                    v-else
                >
                    Привязять к треку
                </AppButton>
                <AppButton
                    @click="save"
                    :active="buttonActive"
                    :loading="updating"
                >
                    Сохранить
                </AppButton>
                <ModalDialog
                    :active="connectToTrackModalOpened"
                    @close="connectToTrackModalOpened = false"
                >
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
const { id } = defineProps({
    id: {
        type: String,
        required: false,
        default: null,
    },
});
const { MAX_CLIP_NAME_LENGTH, YOUTUBE_VIDEO } = useRuntimeConfig().public;
const toast = useToast();
const connectToTrackModalOpened = ref(false);
const clip = id ? ref(await Service.getClipByIdApiV1ClipsClipIdGet(id)) : {};
const title = computed(() =>
    id ? "Редактирование клипа " + clip.value.name : "Создание клипа"
);
const name = ref(id ? clip.value.name : "");
const video_id = computed(() => (id ? clip.value.video_id : null));
const url_raw = computed(() =>
    video_id.value ? YOUTUBE_VIDEO + video_id.value : ""
);
const blob_file = ref(null);
const new_image_url = ref(id ? clip.value.picture : null);
const set_file = (file) => {
    blob_file.value = file;
    new_image_url.value = URL.createObjectURL(file);
};

const get_id_from_youtube_url = (url) => {
    const regex =
        /^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$/;
    const match = url.match(regex);

    if (match) {
        return match[5];
    }
    return null;
};
const url = ref(id ? url_raw.value : "");
const urlCorrect = computed(() => {
    if (!url.value) return false;
    return get_id_from_youtube_url(url.value);
});
const image_type = ref("Файл");
const buttonActive = computed(() => {
    return !!(
        name.value &&
        urlCorrect.value &&
        (id
            ? name.value !== clip.value.name ||
              url.value !== url_raw.value ||
              image_type.value !== "Файл" ||
              blob_file.value
            : image_type.value === "Файл"
            ? blob_file.value
            : image_url_correct.value)
    );
});
const show_click_image_error = () => {
    toast.error(
        'Чтобы изменить изображение, выберите "Файл" в поле "Источник изображения"'
    );
};
const testImageUrl = (url) => {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);
        img.src = url;
    });
};
const image_url_correct = ref(false);
const image_url = computed(() => {
    const video_id = get_id_from_youtube_url(url.value);

    if (!video_id) return null;
    return `https://img.youtube.com/vi/${video_id}/maxresdefault.jpg`;
});
watch(
    image_url,
    async (new_url) => {
        if (!new_url || image_type.value !== "Из видео") return;
        image_url_correct.value = await testImageUrl(new_url);
    },
    { immediate: true }
);
const updating = ref(false);
const save = async () => {
    if (!buttonActive.value) return;
    const new_video_id = get_id_from_youtube_url(url.value);
    if (!new_video_id) {
        toast.error("Неверная ссылка на видео");
        return;
    }
    if (updating.value) return;
    if (id) {
        await update(new_video_id);
    } else {
        await create(new_video_id);
    }
};
const update = async (new_video_id) => {
    updating.value = true;
    const updated_clip = await Service.updateClipApiV1ClipsClipIdPut(id, {
        name: name.value,
        video_id: new_video_id,
        image_from_youtube: image_type.value === "Из видео",
        clipPicture: blob_file.value,
    });
    clip.value = updated_clip;
    image_type.value = "Файл";
    updating.value = false;
    blob_file.value = null;
    new_image_url.value = clip.value.picture;
};
const router = useRouter();
const create = async (new_video_id) => {
    updating.value = true;
    const new_clip = await Service.createClipApiV1ClipsPost({
        name: name.value,
        video_id: new_video_id,
        image_from_youtube: image_type.value === "Из видео",
        clipPicture: blob_file.value,
    });
    updating.value = false;
    router.push({
        name: routesNames.musicianCabinet.cabinetClipsId,
        params: { id: new_clip.id },
    });
};

useHead({
    title: title.value,
});
</script>

<style lang="scss" scoped>
.edit-clip-page {
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 10px;

    @include lg(true) {
        grid-template-columns: 1fr;
    }

    .clip-picture {
        display: flex;
        flex-direction: column;
        --app-select-bg: #{$secondary-bg};

        .clip-picture-image-preview {
            width: 100%;
            height: 100%;
            border-radius: 10px;
            border: 2px dashed transparent;
            overflow: hidden;

            &.error {
                border-color: $accent-red;
            }

            img {
                object-fit: cover;
                width: 100%;
                height: 100%;
            }

            .icon {
                @include flex-center;
                width: 100%;
                height: 100%;
                border-radius: 10px;
                color: #{$secondary-bg};

                svg {
                    color: #8c939d;
                    width: 40px;
                    height: 40px;
                    text-align: center;
                }
            }
        }
    }

    .fields {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
}
</style>
