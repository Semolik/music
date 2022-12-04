<template>
    <FormField placeholder="Поиск" :borderRadius="7" v-model="text" off-margin></FormField>
    <div class="empty" v-if="albumsEmpty">
        <div class="message">
            У вас пока нет альбомов
        </div>
        <router-link class="upload-button" to="/lk/my-music/upload">Загрузить альбом</router-link>
    </div>
    <div class="albums" v-else>
        <Album :albumInfo="album" v-for="album in filteredAlbums" />
    </div>
</template>
<script>
import { HTTP } from '/src/http-common.vue';
import FormField from '/src/components/FormField.vue';
import { useToast } from "vue-toastification";
import handleError from '/src/composables/errors';
import Album from './Item.vue';
export default {
    setup() {
        const toast = useToast();
        return {
            toast
        }
    },
    components: {
        FormField,
        Album
    },
    data() {
        return {
            albums: [],
            text: ''
        }
    },
    mounted() {
        HTTP.get('/albums/get_my_albums')
            .then(response => {
                this.albums = response.data;
            })
            .catch(error => {
                this.toast.error(handleError(error, `При получении альбомов произошла ошибка`).message)
            });
    },
    computed: {
        filteredAlbums() {
            if (!this.text) return this.albums
            return this.albums.filter(album => album.name.toLowerCase().includes(this.text.toLowerCase()))
        },
        albumsEmpty() {
            return this.albums.length === 0;
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';
@use '@/assets/styles/breakpoints';

.albums {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;

    @include breakpoints.md(true) {
        grid-template-columns: repeat(3, 1fr);
    }

    @include breakpoints.sm(true) {
        grid-template-columns: repeat(2, 1fr);
    }
}

.empty {
    border: 2px dashed var(--color-text);
    padding: 10px;
    padding-top: 30px;
    min-height: 100px;
    @include helpers.flex-center;
    border-radius: 15px;
    flex-direction: column;
    gap: 20px;
    height: 100%;

    .upload-button {
        @include components.button;
        border-radius: 10px;
        padding: 5px 10px;
    }
}
</style>