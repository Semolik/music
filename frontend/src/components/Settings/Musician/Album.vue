<template>
    <div class="album-editor" v-if="albumInfo">
        <div class="album-head">
            <div class="picture-container">
                <SelectImage v-if="editorOpened" :pictureUrl="albumInfo.picture" ref="albumPicture" />
                <AlbumPicture :src="albumInfo.picture" offHover v-else />
                <UploadDate v-if="editorOpened && date" :border-radius="10" v-model="date" />
            </div>
            <div class="album-info">
                <div class="headline">
                    <div class="name">{{ albumInfo.name }}</div>
                    <div class="album-buttons">
                        <template v-if="editorOpened">
                            <div class="button" @click="editorOpened = false">
                                <FontAwesomeIcon icon="fa-x" />
                            </div>
                            <div :class="['button', { wrong: isWrong }, { active: buttonActive }]" @click="save">
                                <FontAwesomeIcon icon="fa-floppy-disk" />
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
                    <GenresSelector @change-genre="onGenreChange" ref="genres" :selected-genres-in="albumInfo.genres"
                        force-open />
                </div>
                <div class="extra-info" v-else>
                    <div class="extra-info-item">Год: {{ albumInfo.year }}</div>
                    <div class="extra-info-item">Дата выхода: {{ albumInfo.date }}</div>
                    <router-link :to="`/musician/${albumInfo.musician.id}`" class="extra-info-item">Музыкант: {{ albumInfo.musician.name }}</router-link>
                    <div class="extra-info-item genres" v-if="showGenres">
                        Жанр{{ albumInfo.genres.length > 1 ? 'ы' : '' }}:
                        <div v-for="(genre, index) in albumInfo.genres">
                            <router-link to="">{{ genre.name }}</router-link>
                            <span v-if="index !== albumInfo.genres.length - 1">,</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="message" v-if="editorOpened">Перетяните трек чтобы поменять его положение в альбоме</div>
        <draggable v-model="tracks" :class="['tracks', { draggable: editorOpened }]" item-key="id"
            :disabled="!editorOpened">
            <template #item="{ element }">
                <Track :track-data="element" :musician-data="albumInfo.musician" :album-id="albumInfo.id" />
            </template>
        </draggable>
    </div>
</template>
<script>
import { HTTP } from '/src/http-common.vue';
import { useToast } from "vue-toastification";
import handleError from '/src/composables/errors';
import AlbumPicture from '/src/components/AlbumPicture.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPen, faTrash, faX, faFloppyDisk } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import ModalDialog from '/src/components/ModalDialog.vue';
import Track from '/src/components/Track.vue';
import draggable from 'vuedraggable'
import FormField from '/src/components/FormField.vue';
import GenresSelector from '/src/components/GenresSelector/index.vue';
import UploadDate from './Cabinet/Upload/Date.vue';
import moment from 'moment';
import SelectImage from '/src/components/SelectImage.vue';
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
    components: { AlbumPicture, draggable, FontAwesomeIcon, ModalDialog, Track, FormField, GenresSelector, UploadDate, SelectImage },
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
            tracks: []
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
            var pic = this.$refs.albumPicture?.target;
            return this.albumName !== this.albumInfo.name || this.genresChanged || pic || this.dateChanged || this.tracksPostionChanged;
        },
        dateChanged() {
            return !moment(this.albumInfo.date, this.VITE_DATE_FORMAT).isSame(this.date)
        },
        genresChanged() {
            var newGenresId = this.genres.map(genre => genre.id);
            var oldGenresId = this.albumInfo.genres.map(genre => genre.id);
            return !(JSON.stringify(oldGenresId.sort()) === JSON.stringify(newGenresId.sort()));
        },
        tracksPostionChanged() {
            return !this.arraysEqual(this.tracksToId(this.tracks), this.tracksToId(this.albumInfo.tracks))
        }
    },
    methods: {
        openDeleteDialog() {
            this.deleteDialogOpened = true;
        },
        tracksToId(tracks) {
            return tracks.map(track => track.id)
        },
        arraysEqual(a, b) {
            if (a === b) return true;
            if (a == null || b == null) return false;
            if (a.length !== b.length) return false;
            for (var i = 0; i < a.length; ++i) {
                if (a[i] !== b[i]) return false;
            }
            return true;
        },
        onGenreChange(value) {
            this.genres = value;
        },
        save() {
            if (this.isWrong || !this.buttonActive) return
            var form = new FormData();
            var pic = this.$refs.albumPicture.target;
            form.append('id', this.albumInfo.id);
            form.append('name', this.albumName);
            form.append('date', moment(this.date).format(this.VITE_DATE_FORMAT));
            this.tracks.forEach(track => {
                form.append('tracks_ids', track.id);
            });
            if (pic) {
                form.append('albumPicture', pic[0]);
            }
            this.genres.forEach(element => {
                form.append('genres_ids', element.id);
            });
            HTTP.put('/album', form)
                .then(response => {
                    this.albumInfo = response.data;
                    this.editorOpened = false;
                })
                .catch(error => {
                    this.toast.error(handleError(error).message);
                })
        },

        setData() {
            const { name, date, genres, tracks } = this.albumInfo;
            this.albumName = name;
            this.date = date ? moment(date, this.VITE_DATE_FORMAT).toDate() : null;
            this.genres = genres;
            this.tracks = tracks;
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
@use '@/assets/styles/breakpoints';

.album-editor {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .album-head {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: 10px;

        @include breakpoints.sm(true) {
            grid-template-columns: 1fr;
        }

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


                .extra-info-item {
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

    .message {
        background-color: var(--yellow-dark);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }

    .tracks {
        display: flex;
        flex-direction: column;
        gap: 5px;

        &.draggable {

            .track {
                user-select: none;
                position: relative;

                &::after {
                    position: absolute;
                    cursor: move;
                    content: '';
                    inset: 0;
                }
            }

        }
    }
}
</style>