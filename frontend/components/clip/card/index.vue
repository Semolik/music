<template>
    <nuxt-link :to="link" class="clip-card" v-if="link">
        <ClipCardContent :clip="clip" :musician-info="musicianInfo" />
    </nuxt-link>
    <div class="clip-card" @click="modalOpened = true" v-else>
        <ClipCardContent :clip="clip" :musician-info="musicianInfo" />
    </div>
    <ClipModal
        :clip="clip"
        v-model:modalOpened="modalOpened"
        @update:clip="emit('update:clip', $event)"
    />
</template>
<script setup>
const { clip, musicianInfo } = defineProps({
    clip: {
        type: Object,
        required: true,
    },
    musicianInfo: {
        type: Object,
        required: false,
    },
    link: {
        type: Object,
        required: false,
        default: null,
    },
});
const emit = defineEmits(["update:clip"]);
const modalOpened = ref(false);
</script>
<style lang="scss" scoped>
.clip-card {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 5px;
    border-radius: 10px;
    cursor: pointer;

    &:hover {
        background-color: var(--clip-card-hover-bg, $tertiary-bg);
    }
}
</style>
