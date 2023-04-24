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
                <img
                    :src="image_url"
                    @click="show_click_image_error"
                    v-else
                    class="clip-picture-image-preview"
                />
                <AppSelect
                    :values="['Файл', 'Из видео']"
                    v-model="image_type"
                    title="Источник изображения"
                />
            </div>
            <div class="fields">
                <AppInput v-model="name" label="Название" :error="!name" />
                <AppInput
                    v-model="url"
                    label="Ссылка на видео"
                    :error="!urlCorrect"
                />
                Сделать выбор трека
                <AppButton
                    @click="save"
                    :active="buttonActive"
                    :loading="updating"
                    >Сохранить</AppButton
                >
            </div>
        </div>
    </SettingsPage>
</template>
<script setup>
import { Service } from "~/client";
import { useToast } from "vue-toastification";
import { IconsNames } from "~/configs/icons";
const toast = useToast();
const { YOUTUBE_VIDEO } = useRuntimeConfig().public;
const route = useRoute();
const { id } = route.params;
const clip = ref(await Service.getClipByIdApiV1ClipsClipIdGet(id));
const title = computed(() => "Редактирование клипа " + clip.value.name);
const name = ref(clip.value.name);
const video_id = computed(() => clip.value.video_id);
const url_raw = computed(() => YOUTUBE_VIDEO + video_id.value);
const blob_file = ref(null);
const new_image_url = ref(clip.value.picture);
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
const url = ref(url_raw.value);
const urlCorrect = computed(() => {
    if (!url.value) return false;
    return get_id_from_youtube_url(url.value);
});
const image_type = ref("Файл");
const buttonActive = computed(() => {
    return (
        name.value &&
        urlCorrect.value &&
        (name.value !== clip.value.name ||
            url.value !== url_raw.value ||
            image_type.value !== "Файл" ||
            blob_file.value)
    );
});
const show_click_image_error = () => {
    toast.error(
        'Чтобы изменить изображение, выберите "Файл" в поле "Источник изображения"'
    );
};
const image_url = computed(() => {
    const video_id = get_id_from_youtube_url(url.value);
    if (!video_id) return null;
    return `https://img.youtube.com/vi/${video_id}/maxresdefault.jpg`;
});
const updating = ref(false);
const save = async () => {
    if (!buttonActive.value) return;
    const new_video_id = get_id_from_youtube_url(url.value);
    if (!new_video_id) {
        toast.error("Неверная ссылка на видео");
        return;
    }
    if (updating.value) return;
    updating.value = true;
    const new_clip = await Service.updateClipApiV1ClipsClipIdPut(id, {
        name: name.value,
        video_id: new_video_id,
        image_from_youtube: image_type.value === "Из видео",
        clipPicture: blob_file.value,
    });
    clip.value = new_clip;
    image_type.value = "Файл";
    updating.value = false;
    blob_file.value = null;
    new_image_url.value = clip.value.picture;
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
            object-fit: cover;
            border-radius: 10px;
            aspect-ratio: 16/9;
        }
    }

    .fields {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
}
</style>
