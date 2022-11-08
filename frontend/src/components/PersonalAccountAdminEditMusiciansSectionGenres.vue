<template>
    <div class="headline">Жанры</div>
    <FormField placeholder="Поиск" :borderRadius="10" v-model="searchText"></FormField>
    <div class="genres-list">
        <div class="genre-item" v-for="genre in filteredGenres">
            {{ genre.name }}
        </div>
    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import { useToast } from "vue-toastification";
import handleError from '../composables/errors';
import AlbumPicture from './AlbumPicture.vue';
import FormField from './FormField.vue';

export default {
    setup() {
        const toast = useToast();
        return {
            toast
        };
    },
    data() {
        return {
            genres: [],
            searchText: '',
        };
    },
    mounted() {
        HTTP.get("/genres")
            .then(response => {
                this.genres = response.data;
            })
            .catch(error => {
                this.toast.error(handleError(error).message);
            });
    },
    computed: {
        filteredGenres(){
            if (!this.searchText) return this.genres
            return this.genres.filter(genre => genre.name.includes(this.searchText))
        }
    },
    components: { AlbumPicture, FormField }
}
</script>
<style lang="scss">
@use '@/assets/styles/breakpoints';

.headline {
    text-align: center;
    font-size: x-large;
    font-weight: 600;
    margin-bottom: 20px;
}

.genres-list {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;

    @include breakpoints.md(true) {
        grid-template-columns: repeat(3, 1fr);
    }

    @include breakpoints.sm(true) {
        grid-template-columns: repeat(2, 1fr);
    }

    .genre-item {
        background-color: var(--color-background-mute-3);
        padding: 10px;
        border-radius: 10px;
        text-align: center;

        &:hover {
            background-color: var(--color-background-mute-4);
            cursor: pointer;
            
        }
    }
}
</style>