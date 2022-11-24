<template>
    <div :class="['select-image', { 'empty-pic': !picture }, { wrong: (notEmpty && !target) || warning }]">
        <FontAwesomeIcon icon="fa-image" v-if="!picture" />
        <img :src="picture" v-else>
        <div class="edit-area">
            <div class="edit-area-container">
                <FontAwesomeIcon icon="fa-image" v-if="picture" />
                <div class="edit-area-text">выбрать файл</div>
                <input type="file" :name="name" ref="fileupload" :accept="acceptedFormats" @change="previewFiles">
            </div>
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faImage } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faImage);
import { useToast } from "vue-toastification";
export default {
    setup() {
        const toast = useToast();
        return {
            toast
        }
    },
    props: {
        pictureUrl: String,
        name: String,
        notEmpty: Boolean,
        notEmptyEvent: Boolean,
    },
    emits: ['changed'],
    components: { FontAwesomeIcon },
    data() {
        return {
            picture: this.pictureUrl,
            acceptedFormats: '.jpg, .jpeg, .png',
            target: null,
            warning: false,
        }
    },
    inject: ['runValidation'],
    watch: {
        pictureUrl(value) {
            this.picture = value;
        },
        runValidation(value) {
            console.log(this.notEmptyEvent )
            if (this.notEmptyEvent && value && !this.target) {
                this.warning = true;
            }
        }
    },
    methods: {
        previewFiles(event) {
            let file = event.target.files;
            if (!(file && file[0])) {
                this.detelePicture();
                return;
            }
            
            var fileName = file[0].name;
            var idxDot = fileName.lastIndexOf(".") + 1;
            var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
            let extentions = this.acceptedFormats.split(', ').map(el => el.replace('.', ''));
            if (!extentions.includes(extFile)) {
                this.toast(`Поддерживаемые форматы ${this.acceptedFormats}`);
                this.toast.error('Формат изображения не поддерживанется');
                this.detelePicture()
                return
            }
            this.target = file;
            this.warning = false;
            let reader = new FileReader;
            reader.onload = e => {
                this.picture = e.target.result;
            }
            reader.readAsDataURL(file[0]);
            this.$emit('changed', this.$refs.fileupload)
        },
        detelePicture() {
            this.$refs.fileupload.value = null;
            this.picture = null;
            this.target = null;
        },
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';


.select-image {
    aspect-ratio: 1;
    position: relative;
    overflow: hidden;
    border-radius: 7px;
    transition: 2s filter, 2s opacity;

    img {
        object-fit: cover;
        width: 100%;
        height: 100%;
    }

    &.empty-pic {
        @include helpers.flex-center;
        overflow: hidden;
        border: 2px dashed transparent;
        border-color: var(--color-text);

        svg {
            width: 40%;
            height: 40%;
        }
    }

    &.wrong {
        border: 2px dashed red;
    }

    &:hover {
        .edit-area {
            opacity: 1;
        }

        img {
            filter: blur(3px);
        }
    }

    .edit-area {
        transition: opacity .2s;
        @include helpers.flex-center;
        flex-direction: column;
        position: absolute;
        inset: 0;
        opacity: 0;
        isolation: isolate;

        .edit-area-container {
            z-index: 2;
            position: absolute;
            inset: 0;
            @include helpers.flex-center;
            flex-direction: column;
            background-color: rgba($color: #000000, $alpha: 0.2);
            padding: 5px;
            aspect-ratio: 1;

            svg {
                width: 25%;
                height: 25%;
                margin-bottom: 5%;
                z-index: 2;
            }

            .edit-area-text {
                z-index: 2;
            }

        }

        input {
            position: absolute;
            inset: 0;
            z-index: 3;
            opacity: 0;
            cursor: pointer;
        }

        &::after {
            content: '';
            position: absolute;
            inset: 0;
            background-color: var(--color-background-mute-3);
            opacity: 0.5;
            z-index: 1;
        }
    }
}
</style>