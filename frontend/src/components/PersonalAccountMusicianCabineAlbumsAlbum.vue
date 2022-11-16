<template>
    <div class="album-editor" v-if="albumInfo">
        <div class="album-head">
            <div class="picture-container">
                <AlbumPicture :src="albumInfo.picture" offHover />
                <UploadDate v-if="editorOpened && date" :border-radius="10" v-model="date" />
            </div>
            <div class="album-info">
                <div class="headline">
                    <div class="name">{{ albumInfo.name }}</div>
                    <div class="album-buttons">
                        <template v-if="editorOpened">
                            <div :class="['button', { wrong: isWrong }, { active: buttonActive }]" @click="save">
                                <FontAwesomeIcon icon="fa-floppy-disk" />
                            </div>
                            <div class="button" @click="editorOpened = false">
                                <FontAwesomeIcon icon="fa-x" />
                            </div>
                        </template>
                        <template v-else>
                            <div class="button" @click="editorOpened = true">
                                <FontAwesomeIcon icon="fa-pen" />
                            </div>
                            <div class="button" @click="openDeleteDialog">
                                <FontAwesomeIcon icon="fa-trash" />
                            </div>
                        </template>
                        <ModalDialog @close="closeDeleteDialog" @yes="deleteAlbum" @no="closeDeleteDialog"
                            headline="Удаление альбома" :active="deleteDialogOpened"
                            :text="`Вы точно хотите удалить альбом ${albumInfo.name}?`" yesButton noButton
                            :yesLoading="deleteLoading" />
                    </div>
                </div>
                <div class="extra-info-editor" v-if="editorOpened">
                    <FormField :borderRadius="10" label="Название альбома" off-margin notEmpty v-model="albumName">
                        <span :class="['count', { wrong: upToAlbumLimit < 0 }]" v-if="upToAlbumLimit">
                            {{ upToAlbumLimit }}
                        </span>
                    </FormField>
                    <GenresSelector @change="onGenreChange" :selected-genres-in="albumInfo.genres" force-open />
                </div>
                <div class="extra-info" v-else>
                    <div class="item">Год: {{ albumInfo.year }}</div>
                    <div class="item">Дата выхода: {{ albumInfo.date }}</div>
                    <router-link to="" class="item">Музыкант: {{ albumInfo.musician.name }}</router-link>
                    <div class="item genres" v-if="showGenres">
                        Жанр{{ albumInfo.genres.length > 1 ? 'ы' : '' }}:
                        <div v-for="(genre, index) in albumInfo.genres">
                            <router-link to="">{{ genre.name }}</router-link>
                            <span v-if="index !== albumInfo.genres.length - 1">,</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="tracks">
            <Track :track-data="track" :musician-data="albumInfo.musician" :key="index"
                v-for="(track, index) in albumInfo.tracks" />
        </div>
    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import { useToast } from "vue-toastification";
import handleError from '../composables/errors';
import AlbumPicture from './AlbumPicture.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPen, faTrash, faX, faFloppyDisk } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import ModalDialog from './ModalDialog.vue';
import Track from './Track.vue';
import FormField from './FormField.vue';
import GenresSelector from './GenresSelector.vue';
import UploadDate from './PersonalAccountMusicianCabinetUploadDate.vue';
import moment from 'moment';
library.add(faPen, faTrash, faX, faFloppyDisk);
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
        };
    },
    props: {
        id: {
            type: [Number, String],
        },
    },
    data() {
        return {
            albumInfo: null,
            deleteDialogOpened: false,
            deleteLoading: false,
            editorOpened: false,
            albumName: null,
            date: null,
            genres: [],
        };
    },
    mounted() {
        HTTP.get("album", { params: { id: this.id } })
            .then(response => {
                this.albumInfo = response.data;
                this.setData();

            })
            .catch(error => {
                this.toast.error(handleError(error).message);
            });
    },
    watch: {
        editorOpened() {
            this.setData();
        }
    },
    components: { AlbumPicture, FontAwesomeIcon, ModalDialog, Track, FormField, GenresSelector, UploadDate },
    computed: {
        showGenres() {
            if (!this.albumInfo) return
            return this.albumInfo.genres.length > 0;
        },

        upToAlbumLimit() {
            let length = this.albumName?.length;
            if (!length) return
            return this.VITE_MAX_ALBUM_NAME_LENGTH - length
        },
        isWrong() {
            let length = this.albumName?.length;
            if (!length) return true
        },
        buttonActive() {
            return this.albumName !== this.albumInfo.name || this.genresChanged;
        },
        genresChanged() {
            var newGenresId = this.genres.map(genre => genre.id);
            var oldGenresId = this.albumInfo.genres.map(genre => genre.id);
            return !(JSON.stringify(oldGenresId.sort()) === JSON.stringify(newGenresId.sort()));
        },
    },
    methods: {
        openDeleteDialog() {
            this.deleteDialogOpened = true;
        },
        onGenreChange(value) {
            this.genres = value;
        },
        save() {

        },

        setData() {
            const { name, date } = this.albumInfo;
            this.albumName = name;
            this.date = date ? moment(date, this.VITE_DATE_FORMAT).toDate() : null;
        },
        closeDeleteDialog() {
            this.deleteDialogOpened = false;
        },
        deleteAlbum() {
            HTTP.delete('album', { params: { id: this.albumInfo.id } })
                .then(response => {
                    this.closeDeleteDialog();
                    this.$router.push('/lk/my-music/albums/')
                })
                .catch(error => {
                    this.toast.error(handleError(error).message);
                })
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.album-editor {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .album-head {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: 10px;

        .picture-container {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .album-info {
            display: flex;
            flex-direction: column;

            .headline {
                text-align: center;
                font-weight: 600;
                font-size: x-large;
                margin-bottom: 10px;
                width: 100%;
                @include helpers.flex-center;

                .name {
                    flex-grow: 1;
                }

                .album-buttons {
                    display: flex;
                    gap: 5px;

                    .button {
                        @include components.button;
                        @include components.button-sizes;
                        border-radius: 10px;
                    }
                }
            }

            .extra-info {
                display: flex;
                // justify-content: center;
                flex-wrap: wrap;
                gap: 10px;


                .item {
                    @include helpers.flex-center;
                    flex-grow: 1;
                    color: var(--color-header-text);
                    background-color: var(--color-background-mute-3);
                    padding: 8px 16px;
                    border-radius: 10px;

                    &.genres {
                        display: flex;
                        gap: 5px;
                    }
                }

                a {
                    transition: .2s color;
                    color: var(--color-header-text);
                    text-decoration: none;

                    &:hover {
                        color: var(--yellow);
                    }
                }
            }

            .extra-info-editor {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
        }
    }

    .tracks {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
}
</style>