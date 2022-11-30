<template>
    <form class="add-clip-container">
        <SelectImage :picture-url="imageUrl" :not-empty="notEmpty" :disabled="saveImageFromUrl"
            @changed="image = $event" ref="image" :aspectRatio="'16 / 9'" />
        <div class="clip-content">
            <FormField :force-wrong="!youtubeId" v-model="url" :border-radius="10"
                label="Ссылка на видеоролик с youtube" off-margin />
            <FormField :force-wrong="nameWrong" v-model="name" :border-radius="10" label="Название клипа" off-margin>
                <span :class="['count', { wrong: nameWrong }]" v-if="upToNameLimit">
                    {{ upToNameLimit }}
                </span>
            </FormField>
            <Checkbox v-model="saveImageFromUrl" label="Использовать превью ролика как изображние" />
            <ButtonsBlock :wrong="wrong" :active="buttonActive" @save="handleButton" @delete="deleteClip"
                :delete-button="id !== null" />
        </div>
    </form>
</template>
<script>
import { HTTP } from '/src/http-common.vue';
import Checkbox from '/src/components/checkbox.vue';
import FormField from '/src/components/FormField.vue';
import SelectImage from '/src/components/SelectImage.vue';
import ButtonsBlock from '/src/components/Settings/ButtonsBlock.vue';
export default {
    components: { FormField, SelectImage, ButtonsBlock, Checkbox },
    async setup(props) {
        var clipData = { name: '', url: '', imageUrl: '' };
        if (props.id) {
            const { data } = await HTTP.get('/clips/clip', { params: { id: props.id } });
            clipData = data;
            document.title = `Клип: ${clipData.name}`;
        }
        const { VITE_MAX_CLIP_NAME_LENGTH } = import.meta.env;
        return { VITE_MAX_CLIP_NAME_LENGTH, clipData };
    },
    props: {
        id: {
            default: null,
            types: [String]
        }
    },
    data() {
        return {
            originalClipData: this.clipData,
            name: this.clipData.name,
            url: this.clipData.video,
            imageUrl: this.clipData.picture,
            saveImageFromUrl: false,
            image: null,
            notEmpty: this.id === null,
        }
    },
    watch: {
        saveImageFromUrl(value) {
            if (value) {
                this.notEmpty = true;
            }
        }
    },
    methods: {
        async handleButton() {
            if (!this.buttonActive) return
            var form = new FormData();
            form.append('image_from_youtube', this.saveImageFromUrl);
            form.append('name', this.name);
            form.append('video_id', this.youtubeId);
            let image = this.image?.files[0]
            if (!this.saveImageFromUrl && image) {
                form.append('clipPicture', image);
            }
            if (this.id === null) {
                await this.create(form);
            } else {
                form.append('id', this.originalClipData.id);
                await this.update(form);
            }
        },
        async deleteClip() {
            await HTTP.delete('/clips/clip', { params: { clip_id: this.id } });
            this.$router.push({ path: '/lk/my-music/clips' });
        },
        async update(form) {
            const { data } = await HTTP.put('/clips/clip', form);
            const { name, picture, video } = data;
            this.$refs.image.detelePicture();
            this.name = name;
            this.imageUrl = picture;
            this.url = video;
            this.originalClipData = data;
            this.saveImageFromUrl = false;
            this.notEmpty = false;
        },
        async create(form) {
            const { data: { id } } = await HTTP.post('/clips/clip', form);
            this.$router.push({ path: `/lk/my-music/clips/${id}` })
        }
    },
    computed: {
        youtubeId() {
            var result = /http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?/.exec(this.url)
            return result ? result[1] : null
        },
        wrong() {
            return !this.youtubeId || !(this.saveImageFromUrl ? true : this.notEmpty ? this.image : true) || this.nameWrong;
        },
        buttonActive() {
            if (!this.id) return !this.wrong
            return (this.url !== this.originalClipData.video || this.name !== this.originalClipData.name || this.notEmpty || this.image) && !this.wrong;
        },
        upToNameLimit() {
            let length = this.name?.length;
            if (!length) return
            return this.VITE_MAX_CLIP_NAME_LENGTH - length
        },
        nameWrong() {
            return this.upToNameLimit < 0 || this.name.length === 0
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/components';

.add-clip-container {
    @include components.container-with-select-image(300px);

    .clip-content {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
}
</style>