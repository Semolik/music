<template>
    <div class="genres-selector">
        <FormField id="genres-selector" :inputEvents="{ focus: onFocus }" v-on-click-outside="onBlur"
            :class="{ active: focused }" v-model="searchText" placeholder="Поиск по жанрам" :borderRadius="borderRadius"
            label="Жанры" :formkitInnerClass="{ focused: focused }" borderColor="transparent" off-margin offChangeColor>
            <div class="search-items" v-if="focused">
                <SearchItem :genre="genre" v-for="(genre, index) in filteredGenres" :key="index"
                    :selectedGenres="selectedGenres" @selectGenre="selectGenre(genre)" />
            </div>
        </FormField>
        <div class="selected-genres" v-if="!focused && selectedGenres.length !== 0" v-auto-animate>
            <SearchItem :genre="genre" v-for="(genre, index) in selectedGenres" :key="index"
                :selectedGenres="selectedGenres" @selectGenre="selectGenre(genre)" />
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
@use '@/assets/styles/breakpoints';

.genres-selector {
    @mixin columns {
        grid-template-columns: repeat(4, 1fr);

        @include breakpoints.md(true) {
            grid-template-columns: repeat(3, 1fr);
        }

        @include breakpoints.sm(true) {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    border: 1px solid var(--fields-border-color);
    border-radius: 10px;

    .selected-genres {
        display: grid;
        @include columns;
        gap: 10px;
    }

    .formkit-inner {
        flex-direction: column;
        position: relative;

        input {
            background-color: rgba($color: #000000, $alpha: 0.1);
        }

        &.focused {
            overflow: inherit !important;

            .formkit-input {
                border-radius: 5px 5px 0 0;
            }

            input {
                border-radius: 5px 5px 0 0;
                background-color: rgba($color: #000000, $alpha: 0.2);
                border: 1px solid var(--fields-border-color);
                border-bottom: none;
            }
        }

        .search-items {
            width: 100%;
            border: 1px solid var(--fields-border-color);
            border-top: none;
            border-radius: 0 0 5px 5px;
            max-height: 110px;
            height: 110px;
            overflow: auto;
            padding: 10px;
            gap: 10px;
            display: grid;
            @include columns;
        }
    }
}
</style>