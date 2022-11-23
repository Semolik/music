<template>
    <div :class="['item', { active: active }, { wrong: wrong }]" @click="select">
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
    emits: ['selectGenre'],
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
            if (!this.active && this.selectedGenres.length >= this.VITE_MAX_SELECT_GENRES_COUNT) {
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
        active() {
            return this.selectedGenres.map(genre => genre.id).includes(this.genre.id)
        }
    }
}
</script>
<style lang="scss">
.item {
    &:first-child {
        border: none;
    }

    &.active {
        background-color: var(--purple);
    }

    &.wrong {
        background-color: var(--red-0) !important;
    }

    cursor: pointer;
    border-top: 1px solid var(--accent-color);
    padding: 10px 20px;
    text-align: center;
    background-color: var(--color-background-mute-4);
    border-radius: 5px;
    height: min-content;
    user-select: none;

    &:not(.active):hover {
        background-color: var(--color-background-mute-5);
    }
}
</style>