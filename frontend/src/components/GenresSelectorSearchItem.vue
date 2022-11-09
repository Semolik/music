<template>
    <div :class="['item', { disabled: disabled }, { wrong: wrong }]" @click="select">
        {{ genre.name }}
    </div>
</template>
<script>
import { useToast } from "vue-toastification";
export default {
    props: {
        genre: Object,
        selectedGenres: Array,
    },
    data() {
        return {
            wrong: false
        }
    },
    setup() {
        const toast = useToast();
        const {
            VITE_MAX_SELECT_GENRES_COUNT,
        } = import.meta.env;
        return {
            toast,
            VITE_MAX_SELECT_GENRES_COUNT: parseInt(VITE_MAX_SELECT_GENRES_COUNT)
        };
    },
    methods: {
        select() {
            if (!this.disabled && this.selectedGenres.length >= this.VITE_MAX_SELECT_GENRES_COUNT) {
                this.wrong = true;
                this.toast.error(`Можно выбрать до ${this.VITE_MAX_SELECT_GENRES_COUNT} жанров`)
                setTimeout(() => {
                    this.wrong = false;
                }, 500)
            } else {
                this.$emit('selectGenre', true);
            }
        }
    },
    computed: {
        disabled() {
            return this.selectedGenres.includes(this.genre)
        }
    }
}
</script>
<style lang="scss">
.item {
    &:first-child {
        border: none;
    }

    &.disabled {
        background-color: var(--color-background-mute);
        cursor: auto;
    }

    &.wrong {
        background-color: var(--red-0) !important;
    }

    cursor: pointer;
    border-top: 1px solid var(--accent-color);
    padding: 10px;
    background-color: var(--color-background-mute-3);

    &:not(.disabled):hover {
        background-color: var(--color-background-mute-4);
    }
}
</style>