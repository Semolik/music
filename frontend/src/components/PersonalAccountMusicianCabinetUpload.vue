<template>
    <div class="buttons">
        <div :class="['button', { active: activeSelection === 'single' }]" @click="activeSelection = 'single'">
            <div class="text">Сингл</div>
        </div>
        <div :class="['button', { active: activeSelection === 'album' }]" @click="activeSelection = 'album'">
            <div class="text">Альбом</div>
        </div>
    </div>
    <div class="songs">
        <template v-if="singleMode">
            <SelectDate v-model="date" />
            <UploadSong :track="track" ref="track" @update="trackUpdate($event)" is-single />
        </template>
        <template v-else>
            <div class="columns">
                <SelectImage @changed="updatedPicture" ref="selectPicAlbum" notEmpty />
                <div class="container" id="upload-album">
                    <FormField :borderRadius="10" label="Название альбома" off-margin notEmpty v-model="albumName">
                        <span :class="['count', { wrong: upToAlbumLimit < 0 }]" v-if="upToAlbumLimit">
                            {{ upToAlbumLimit }}
                        </span>
                    </FormField>
                    <SelectDate v-model="date" />
                </div>
            </div>
            <UploadSong :ref="`track-${index}`" :id="index" :track="track" @update="trackUpdate($event, index)"
                v-for="(track, index) in tracks" />
        </template>
        <div class="buttons-container">
            <div class="button-block" @click="addTrack" v-if="!singleMode">
                <FontAwesomeIcon icon="fa-plus" />
            </div>
            <div :class="['button-block', { active: buttonActive }]" @click="save">
                <FontAwesomeIcon icon="fa-floppy-disk" />
            </div>
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { faFloppyDisk } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { computed } from '@vue/reactivity';
import UploadSong from './PersonalAccountMusicianCabinetUploadSong.vue'
import { HTTP } from '../http-common.vue';
import FormField from './FormField.vue';
import { useToast } from "vue-toastification";
import SelectImage from './SelectImage.vue';
import moment from 'moment';
import SelectDate from './PersonalAccountMusicianCabinetUploadDate.vue';

library.add(faPlus, faFloppyDisk);
export default {
    setup() {
        const toast = useToast();
        const {
            VITE_DATE_FORMAT,
            VITE_MAX_ALBUM_NAME_LENGTH
        } = import.meta.env;
        return {
            toast,
            VITE_DATE_FORMAT,
            VITE_MAX_ALBUM_NAME_LENGTH
        }
    },
    components: { FormField, UploadSong, FontAwesomeIcon, SelectImage, SelectDate },
    data() {
        return {
            activeSelection: "single",
            albumName: "",
            tracks: [{}],
            track: {},
            runValidation: false,
            date: new Date(),
            album_id: null,
            mounted: false,
            albumLimit: this.VITE_MAX_ALBUM_NAME_LENGTH,
        };
    },
    provide() {
        return {
            runValidation: computed(() => this.runValidation),
            album_id: computed(() => this.album_id),
            album_date: computed(() => this.date),
        }
    },
    mounted() {
        this.mounted = true
    },
    watch: {
        singleMode(value) {
            this.tracks = [{}];
            this.track = {};
            this.albumName = "";
        },

    },
    methods: {
        toggleRunValidation() {
            this.runValidation = false;
            this.runValidation = true;
            setTimeout(() => {
                this.runValidation = false;
            }, 300)
        },
        updatedPicture(target) {
            this.album_pucture = target;
        },
        trackUpdate(event, index) {
            if (this.singleMode) {
                this.track = event;
                this.albumName = event.album;
            } else {
                this.tracks[index] = event;
            }
        },
        addTrack() {
            this.tracks.push(this.trackTemplate);
        },
        async save() {
            this.toggleRunValidation();
            if (this.buttonActive) {
                var formData = new FormData();
                formData.append('name', this.albumName);
                let picture = this.$refs.selectPicAlbum?.target[0];
                if (picture) {
                    formData.append('albumPicture', picture);
                }
                formData.append('date', moment(this.date).format(this.VITE_DATE_FORMAT));
                let album = await HTTP.post('/create_album', formData)
                    .then(response => response.data)
                    .catch(error => { });
                if (!album) {
                    this.toast.error('Произошла ошибка при создании альбома');
                }
                this.album_id = album.id;
                if (this.singleMode) {
                    this.$refs.track.sendFile();
                }
                else {
                    for (let index = 0; index < this.tracks.length; index++) {
                        this.$refs[`track-${index}`][0].sendFile();
                    }
                }
            }
        }
    },

    computed: {
        singleMode() {
            return this.activeSelection === 'single'
        },
        buttonActive() {
            if (this.activeSelection === 'single') {
                return this.track.isValid
            }
            else {
                return this.tracks.filter(el => el?.isValid).length == this.tracks.length && this.albumName.length > 0
            }
        },
        upToAlbumLimit() {
            let length = this.albumName?.length;
            if (!length) return
            return this.albumLimit - length
        },
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/components';
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';


.buttons {
    display: grid;
    gap: 5px;
    grid-template-columns: repeat(2, 1fr);

    .button {
        @include components.button;
    }

}

.songs {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .columns {
        display: grid;
        grid-template-columns: 140px 1fr;
        gap: 10px;

        .container {
            display: flex;
            gap: 10px;
            width: 100%;
            flex-direction: column;
        }

        @include breakpoints.md(true) {
            grid-template-columns: 1fr;
        }


    }

    .buttons-container {
        display: flex;
        justify-content: right;
        gap: 5px;

        .button-block {
            @include components.button;
            @include helpers.flex-center;
            height: 45px;
            width: 45px;

            &.active {
                background-color: var(--purple-1);
            }

            svg {
                width: 20px;
                height: 20px;
            }
        }
    }
}
</style>