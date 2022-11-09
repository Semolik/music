<template>
    <div class="genres-selector">
        <FormField id="genres-selector" :inputEvents="{ focus: onFocus }" v-on-click-outside="onBlur"
            :class="{ active: focused }" v-model="searchText" placeholder="Поиск по жанрам" :borderRadius="borderRadius"
            label="Жанры" :formkitInnerClass="{ focused: focused }" off-margin offChangeColor>
            <template v-if="focused">
                <label class="search-items" for="genres-selector">
                    <SearchItem :genre="genre" v-for="genre in filteredGenres" :selectedGenres="selectedGenres"
                        @selectGenre="selectGenre(genre)" />
                </label>
            </template>
        </FormField>
        <div class="selected-genres" v-if="selectedGenres.length !== 0">
            <div class="item" v-for="genre in selectedGenres" @click="deleteGenre(genre)">{{ genre.name }}</div>
        </div>
    </div>
</template>
<script>
import { HTTP } from '../http-common.vue';
import FormField from './FormField.vue';
import { useToast } from "vue-toastification";
import handleError from '../composables/errors';
import { vOnClickOutside } from '@vueuse/components';
import SearchItem from './GenresSelectorSearchItem.vue';

export default {
    props: {
        borderRadius: Number,
    },
    components: { FormField, SearchItem },
    setup() {
        const toast = useToast();
        return {
            toast
        };
    },
    directives: {
        OnClickOutside: vOnClickOutside,
    },
    data() {
        return {
            genres: [],
            focused: false,
            searchText: '',
            selectedGenres: [],
            interval: null,
        }
    },
    computed: {
        filteredGenres() {
            return this.genres.filter(genre => genre.name.includes(this.searchText))
        }
    },
    methods: {
        onFocus() {
            this.focused = true;
            if (this.interval !== null) {
                clearInterval(this.interval);
            }
        },
        onBlur() {
            this.focused = false;
        },
        selectGenre(genre) {
            if (this.selectedGenres.includes(genre)) {
                this.deleteGenre(genre);
            } else {
                this.selectedGenres.push(genre);
            }

        },
        deleteGenre(genre) {
            this.selectedGenres = this.selectedGenres.filter(selectedGenre => selectedGenre.id !== genre.id);
        }
    },
    mounted() {
        HTTP.get("/genres")
            .then(response => {
                this.genres = response.data;
            })
            .catch(error => {
                this.toast.error(handleError(error).message);
            });
    }
}
</script>
<style lang="scss">
.genres-selector {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .selected-genres {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;

        .item {
            flex-grow: 1;
            min-width: 100px;
            text-align: center;
            border-radius: 10px;
            padding: 10px;
            background-color: var(--purple);
        }
    }

    .formkit-inner {
        flex-direction: column;
        position: relative;

        &.focused {
            overflow: inherit !important;
            border-radius: var(--inner-radius) var(--inner-radius) 0 0 !important;
        }

        .search-items {
            top: 100%;
            position: absolute;
            display: flex;
            flex-direction: column;
            width: 100%;
            outline: 1px solid var(--accent-color);
            z-index: 99;
            border-radius: 0 0 var(--inner-radius) var(--inner-radius);
            max-height: 114px;
            overflow: auto;
        }
    }
}
</style>