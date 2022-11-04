<template>
    <div class="upload-song-container">
        <FormField @empty="nameIsValid = $event" :borderRadius="borderRadius" label="Название" v-model="data.name"
            off-margin notEmpty>
            <span :class="['count', { wrong: upToNameLimit < 0 }]" v-if="nameLenght">{{ upToNameLimit }}</span>
        </FormField>
        <div class="block">
            <SelectImage @changed="pictureUpdated" :pictureUrl="data.picture" name="userPicture" ref="selectPic"
                notEmpty />
            <div class="fields-container" :id="`fields-${id}`">
                <FormField @empty="albumIsValid = $event" v-model="data.album" :borderRadius="borderRadius"
                    label="Альбом" off-margin notEmpty v-if="isSingle">
                    <span :class="['count', { wrong: upToAlbumLimit < 0 }]" v-if="albumLenght">{{ upToAlbumLimit
                    }}</span>
                    <template v-slot:side>
                        <div :class="['button', { active: followingName }]" @click="clickFollowingButton">
                            <FontAwesomeIcon icon='fa-paperclip' />
                        </div>
                    </template>
                </FormField>
                <FormField @empty="featIsValid = $event" :borderRadius="borderRadius" label="Создан совместно с"
                    v-model="data.feat" off-margin>
                    <span :class="['count', { wrong: upToFeatLimit < 0 }]" v-if="featLenght">{{ upToFeatLimit }}</span>
                </FormField>
            </div>
        </div>
        <Teleport :disabled="isSingle" :to="`#fields-${id}`" v-if="mounted">
            <div :class="['music-selector', { setMinHeight: isSingle }, { active: fileName }, { wrong: wrongFile }, { progress: uploadPercentage > 0 }]"
                :style="{ '--progress': uploadPercentage + '%' }">
                <div class="text">{{ fileName || 'выбрать аудиофайл' }}</div>
                <input type="file" @change="validFile" :ref="refAudioName" :accept="acceptedFormats">
            </div>
        </Teleport>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPaperclip } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import SelectImage from './SelectImage.vue';
import FormField from './FormField.vue';
import { useToast } from "vue-toastification";
import { HTTP } from '../http-common.vue';
import moment from 'moment';
import handleError from '../composables/errors';

library.add(faPaperclip);

export default {
    props: {
        isSingle: Boolean,
        id: Number,
    },
    setup() {
        const toast = useToast();
        const {
            VITE_MAX_TRACK_NAME_LENGTH,
            VITE_MAX_TRACK_FEAT_LENGTH,
            VITE_MAX_ALBUM_NAME_LENGTH,
            VITE_DATE_FORMAT
        } = import.meta.env;
        return {
            VITE_MAX_TRACK_NAME_LENGTH,
            VITE_MAX_TRACK_FEAT_LENGTH,
            VITE_MAX_ALBUM_NAME_LENGTH,
            VITE_DATE_FORMAT,
            toast
        }
    },
    mounted() {
        this.mounted = true;
        this.updateDataParent();
    },
    data() {
        return {
            data: {
                picture: null,
                name: '',
                feat: '',
                album: '',
                file: null,
                isValid: false,
                audioFileTarget: null,
                pictureTarget: null,
            },
            wrongFile: false,
            refAudioName: `audio-${this.id}`,
            fileName: null,
            mounted: false,
            nameIsValid: false,
            featIsValid: false,
            albumIsValid: false,
            borderRadius: 5,
            nameLimit: this.VITE_MAX_TRACK_NAME_LENGTH,
            albumLimit: this.VITE_MAX_ALBUM_NAME_LENGTH,
            featLimit: this.VITE_MAX_TRACK_FEAT_LENGTH,
            followingName: this.isSingle,
            acceptedFormats: '.mp3, .ogg',
            uploadPercentage: 0,
        };
    },
    components: { SelectImage, FormField, FontAwesomeIcon },
    inject: ['runValidation', 'album_id', 'album_date'],
    watch: {
        data: {
            handler() {
                this.updateDataParent();
            },
            deep: true,
        },
        'data.name'() {
            if (this.followingName) {
                this.setFollowingAlbumName();
            }
        },
        trackIsValid(value) {
            this.data.isValid = value;
        },
        runValidation(value) {
            if (value && !this.data.audioFileTarget) {
                this.wrongFile = true;
            }
        }
    },
    methods: {
        pictureUpdated(file) {
            this.data.pictureTarget = file;
        },
        sendFile() {
            if (this.album_id) {
                let data = this.data;
                let form = new FormData();
                form.append('name', data.name);
                form.append('album_id', this.album_id);
                form.append('feat', data.feat);
                form.append('track', data.audioFileTarget);
                form.append('date', moment(this.album_date).format(this.VITE_DATE_FORMAT));
                HTTP.post('upload_song', form, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    },
                    onUploadProgress: function (progressEvent) {
                        this.uploadPercentage = parseInt(Math.round((progressEvent.loaded / progressEvent.total) * 100));
                    }.bind(this)
                })
                    .then((response) => {
                        // this.toast(response.data?.detail);
                        this.uploadPercentage = 0;
                    })
                    .catch((error) => {
                        this.toast.error(handleError(error, `При загрузке трека ${this.fileName} произошла ошибка`).message)

                    });
            }
        },
        updateDataParent() {
            this.$emit('update', this.data);
        },
        setFollowingAlbumName() {
            let name = this.data.name;
            this.data.album = name ? name + ' - сингл' : '';
        },
        clickFollowingButton() {
            this.followingName = !this.followingName;
            if (this.followingName && this.name) {
                this.setFollowingAlbumName();
            }
        },
        resetInputAudio() {
            this.$refs[this.refAudioName].value = null;
            this.fileName = null;
            this.data.audioFileTarget = null;
        },
        validFile(event) {
            let file = event.target.files;
            this.data.audioFileTarget = null;
            if (!(file && file[0])) {
                this.resetInputAudio();
                return;
            }
            var fileName = file[0].name;
            var idxDot = fileName.lastIndexOf(".") + 1;
            var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
            let extentions = this.acceptedFormats.split(', ').map(el => el.replace('.', ''));
            if (!extentions.includes(extFile)) {
                this.toast(`Поддерживаемые форматы ${this.acceptedFormats}`);
                this.toast.error('Данный формат аудио не поддерживанется');
                this.resetInputAudio();
                return
            }
            this.wrongFile = false;
            this.fileName = fileName;
            this.data.audioFileTarget = file[0];
        }
    },
    computed: {
        nameLenght() {
            return this.data.name.length
        },
        featLenght() {
            return this.data.feat.length
        },
        albumLenght() {
            return this.data.album.length
        },
        upToNameLimit() {
            return this.nameLimit - this.nameLenght
        },
        upToFeatLimit() {
            return this.featLimit - this.featLenght
        },
        upToAlbumLimit() {
            return this.albumLimit - this.albumLenght
        },
        trackIsValid() {
            var result = (this.nameLenght > 0 && this.upToNameLimit >= 0) && (this.upToFeatLimit >= 0) && this.data?.audioFileTarget;
            if (this.isSingle) {
                result = result && this.upToAlbumLimit >= 0;
            }
            return result;
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';

.upload-song-container {

    background-color: var(--color-background-mute-3);
    border-radius: 10px;
    border: 1px solid var(--color-background-mute-6);
    padding: 10px;
    display: grid;
    gap: 10px;

    .block {
        display: grid;
        grid-template-columns: 140px 1fr;
        gap: 10px;

        @include breakpoints.rwd(450, true) {
            grid-template-columns: 1fr;
        }

        .fields-container {
            display: flex;
            flex-direction: column;
            gap: 10px;

            .button {
                box-shadow: 0 0 0 1px var(--fields-border-color);
                border-radius: 5px;
                padding: 0px 10px;
                @include helpers.flex-center;
                cursor: pointer;

                &.active {
                    background-color: var(--purple-1);
                    box-shadow: 0 0 0 1px var(--purple-1);
                }

                svg {
                    width: 18px;
                    height: 18px;
                }
            }
        }
    }

    .music-selector {
        padding: 10px;
        border: 2px dashed var(--color-text);
        border-radius: 10px;
        height: 100%;
        @include helpers.flex-center;
        position: relative;


        &.wrong {
            border: 2px dashed red;
        }

        &.active {
            border-color: var(--green);

            &.progress {
                overflow: hidden;
                isolation: isolate;

                &::after {
                    z-index: -1;
                    content: '';
                    position: absolute;
                    height: 100%;
                    background-color: var(--green-128-hover);
                    width: var(--progress);
                    left: 0;
                }
            }
        }

        &:hover {
            background-color: var(--color-background-mute);
        }

        &.setMinHeight {
            min-height: 80px;
        }

        input {
            cursor: pointer;
            position: absolute;
            inset: 0;
            opacity: 0;
        }
    }
}
</style>