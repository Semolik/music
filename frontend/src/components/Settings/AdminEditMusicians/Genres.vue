<template>
    <div class="headline">
        <div class="text">Жанры</div>
        <router-link to="/lk/edit-musician-section/genres/add" class="add-genre-button">
            <FontAwesomeIcon icon="fa-plus" />
        </router-link>
    </div>
    <FormField placeholder="Поиск" :borderRadius="10" v-model="searchText"></FormField>
    <div class="genres-list" v-auto-animate>
        <router-link :to="`/lk/edit-musician-section/genres/${genre.id}`" class="genre-item"
            v-for="(genre, index) in filteredGenres" :key="index">
            {{ genre.name }}
        </router-link>
    </div>
</template>
<script>
import { HTTP } from '/src/http-common.vue';
import { useToast } from "vue-toastification";
import handleError from '/src/composables/errors';
import AlbumPicture from '/src/components/AlbumPicture.vue';
import FormField from '/src/components/FormField.vue';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faPlus);

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
        HTTP.get("/genres/all")
            .then(response => {
                this.genres = response.data;
            })
            .catch(error => {
                this.toast.error(handleError(error).message);
            });
    },
    computed: {
        filteredGenres() {
            if (!this.searchText) return this.genres
            return this.genres.filter(genre => genre.name.includes(this.searchText))
        }
    },
    components: { AlbumPicture, FormField, FontAwesomeIcon }


}
</script>
<style lang="scss">
@use '@/assets/styles/animations';
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/components';
@use '@/assets/styles/helpers';
@include animations.list;
.headline {
    display: flex;

    .text {
        text-align: center;
        font-size: x-large;
        font-weight: 600;
        margin-bottom: 20px;
        width: 100%;
    }

    .add-genre-button {
        @include components.button;
        @include helpers.flex-center;
        border-radius: 10px;
        padding: 5px;

        width: 40px;
        height: 40px;

    }
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
        color: var(--color-text);
        text-decoration: none;
        background-color: var(--color-background-mute-3);
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        height: min-content;

        &:hover {
            background-color: var(--color-background-mute-4);
            cursor: pointer;
        }
    }
}
</style>