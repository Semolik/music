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
        <UploadSong :track="track" ref="track" @update="trackUpdate($event)" is-single v-if="singleMode" />
        <template v-else>
            <div class="columns">
                <SelectImage @changed="updatedPicture" ref="selectPicAlbum" notEmpty />
                <div class="container" id="upload-album">
                    <FormField :borderRadius="10" label="Название альбома" off-margin notEmpty v-model="albumName">
                        <span :class="['count', { wrong: upToAlbumLimit < 0 }]" v-if="upToAlbumLimit">
                            {{ upToAlbumLimit }}
                        </span>
                    </FormField>
                    <div class="group">
                        <SelectDate v-model="date" :borderRadius="10" />
                        <GenresSelector :borderRadius="borderRadius" :border-radius="10" ref="genres" />
                    </div>
                </div>
            </div>
            <UploadSong :ref="`track-${index}`" :id="index" :track="track" @update="trackUpdate($event, index)"
                v-for="(track, index) in tracks" />
        </template>
        <div class="buttons-container">
            <div class="button-block" @[!loadingActive&&`click`]="addTrack" v-if="!singleMode">
                <FontAwesomeIcon icon="fa-plus" />
            </div>
            <div :class="['button-block', { active: buttonActive }, { loading: loadingActive }]"
                @[!loadingActive&&`click`]="save">
                <FontAwesomeIcon :icon="loadingActive ? 'spinner' : 'fa-floppy-disk'" />
            </div>
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { faFloppyDisk, faSpinner } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { computed } from '@vue/reactivity';
import UploadSong from './PersonalAccountMusicianCabinetUploadSong.vue'
import { HTTP } from '../http-common.vue';
import FormField from './FormField.vue';
import { useToast } from "vue-toastification";
import SelectImage from './SelectImage.vue';
import moment from 'moment';
import SelectDate from './PersonalAccountMusicianCabinetUploadDate.vue';
import GenresSelector from './GenresSelector.vue';

library.add(faPlus, faFloppyDisk, faSpinner);
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
    components: { FormField, UploadSong, FontAwesomeIcon, SelectImage, SelectDate, GenresSelector },
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
        allTracksUploaded(value) {
            if (value) {
                // this.toast(`Загрузка трек${this.singleMode ? "а" : "ов"} завершена`);
                this.$router.push({ path: `/lk/my-music/albums/${this.album_id}` });
            }
        }
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
            if (this.buttonActive && !this.loadingActive) {
                var formData = new FormData();
                formData.append('name', this.albumName);
                if (this.singleMode) {
                    let track = this.$refs.track;
                    var picture = track.trackPicture;
                    track.$refs.genres.selectedGenres.forEach(element => {
                        formData.append('genres_ids', element.id);
                    });
                } else {
                    var picture = this.$refs.selectPicAlbum?.target;
                }

                if (picture) {
                    formData.append('albumPicture', picture[0]);
                }

                let date = this.singleMode ? this.track.date : this.date;
                formData.append('date', moment(date).format(this.VITE_DATE_FORMAT));
                let album = await HTTP.post('/album', formData)
                    .then(response => response.data)
                    .catch(error => {
                        return null
                    });
                if (!album) {
                    this.toast.error('Произошла ошибка при создании альбома');
                    return
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
            if (this.allTracksUploaded) {
                return
            }
            if (this.singleMode) {
                return this.track.isValid
            }
            else {
                return this.tracks.filter(el => el?.isValid).length == this.tracks.length && this.albumName.length > 0
            }
        },
        loadingActive() {
            if (this.singleMode) {
                return this.track.loading
            }
            else {
                return this.tracks.filter(el => el?.loading).length == this.tracks.length
            }
        },
        allTracksUploaded() {
            if (this.singleMode) {
                return this.track.uploaded
            }
            else {
                return this.tracks.filter(el => el?.uploaded).length == this.tracks.length
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

        @include breakpoints.sm(true) {
            grid-template-columns: 1fr;
        }

        .group {
            display: grid;
            grid-template-columns: 180px 1fr;
            gap: 10px;

            @include breakpoints.sm(true) {
                grid-template-columns: 1fr;
            }
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

            &.active:not(.loading) {
                background-color: var(--purple-1);
            }

            &.loading {
                svg {

                    @keyframes spin {
                        from {
                            transform: rotate(0deg);
                        }

                        to {
                            transform: rotate(360deg);
                        }
                    }

                    animation-name: spin;
                    animation-duration: 1s;
                    animation-iteration-count: infinite;
                    animation-timing-function: linear;

                }
            }

            svg {
                width: 20px;
                height: 20px;
            }
        }
    }
}
</style>