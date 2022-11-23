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
import { HTTP } from '/src/http-common.vue';
import FormField from '/src/components/FormField.vue';
import { useToast } from "vue-toastification";
import handleError from '/src/composables/errors';
import { vOnClickOutside } from '@vueuse/components';
import SearchItem from './SearchItem.vue';

export default {
    props: {
        borderRadius: Number,
        selectedGenresIn: Array,
        forceOpen: Boolean,
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
    emits: ['change-genre'],
    data() {
        return {
            genres: [],
            focused: this.forceOpen,
            searchText: '',
            selectedGenres: this.selectedGenresIn || [],
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
            if (!this.forceOpen) {
                this.focused = true;
                if (this.interval !== null) {
                    clearInterval(this.interval);
                }
            }
        },
        onBlur() {
            if (!this.forceOpen) {
                this.focused = false;
            }
        },
        selectGenre(genre) {
            if (this.selectedGenres.map(genre => genre.id).includes(genre.id)) {
                this.deleteGenre(genre);
            } else {
                this.selectedGenres.push(genre);
                this.$emit('change-genre', this.selectedGenres);
            }
        },
        deleteGenre(genre) {
            const result = this.selectedGenres.filter(selectedGenre => selectedGenre.id !== genre.id)
            this.selectedGenres = result;
            this.$emit('change-genre', result);
        }
    },
    mounted() {
        HTTP.get("/genres")
            .then(response => {
                this.$emit('change-genre', this.selectedGenres);
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
            height: min-content;
            min-height: 60px;
            overflow: auto;
            padding: 10px;
            gap: 10px;
            display: grid;
            @include columns;
        }
    }
}
</style>