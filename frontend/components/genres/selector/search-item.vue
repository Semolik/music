<template>
    <div
        :class="['genre-card', { active: active }]"
        @click="emit(active ? 'remove' : 'add', genre)"
    >
        {{ genre.name }}
    </div>
</template>
<script setup>
const { active, genre } = defineProps({
    active: {
        type: Boolean,
        required: true,
    },
    genre: {
        type: Object,
        required: true,
    },
});

const emit = defineEmits(["add", "remove"]);
</script>
<style scoped lang="scss">
.genre-card {
    padding: 10px;
    @include flex-center;
    border-radius: 10px;
    background-color: $quaternary-bg;
    cursor: pointer;
    user-select: none;
    height: min-content;
    &:hover {
        background-color: $quinary-bg;
    }
    &.active {
        background-color: $accent;
        color: $primary-bg;
        &:hover {
            background-color: $accent-hover;
        }
    }
}
</style>
