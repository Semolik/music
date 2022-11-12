<template>
    <div class="album-editor" v-if="albumInfo">
        <div class="album-head">
            <AlbumPicture :src="albumInfo.picture" offHover />
            <div class="album-info">
                <div class="headline">
                    <div class="name">{{ albumInfo.name }}</div>
                    <div class="album-buttons">
                        <div class="button">
                            <FontAwesomeIcon icon="fa-pen" />
                        </div>
                        <div class="button" @click="openDeleteDialog">
                            <FontAwesomeIcon icon="fa-trash" />
                        </div>
                        <ModalDialog @close="closeDeleteDialog" @no="closeDeleteDialog" headline="Удаление альбома"
                            :active="deleteDialogOpened" :text="`Вы точно хотите удалить альбом ${albumInfo.name}?`"
                            yesButton noButton />
                    </div>
                </div>
                <div class="extra-info">
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
    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import { useToast } from "vue-toastification";
import handleError from '../composables/errors';
import AlbumPicture from './AlbumPicture.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faPen, faTrash } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import ModalDialog from './ModalDialog.vue';
library.add(faPen, faTrash);
export default {
    setup() {
        const toast = useToast();
        return {
            toast
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
        };
    },
    mounted() {
        HTTP.get("album", { params: { id: this.id } })
            .then(response => {
                this.albumInfo = response.data;
            })
            .catch(error => {
                this.toast.error(handleError(error).message);
            });
    },
    components: { AlbumPicture, FontAwesomeIcon, ModalDialog },
    computed: {
        showGenres() {
            if (!this.albumInfo) return
            return this.albumInfo.genres.length > 0;
        }
    },
    methods: {
        openDeleteDialog() {
            this.deleteDialogOpened = true;
        },
        closeDeleteDialog() {
            this.deleteDialogOpened = false;
        },
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.album-editor {
    display: flex;
    flex-direction: column;

    .album-head {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: 10px;

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
                        color: #fc0;
                    }
                }
            }
        }
    }
}
</style>