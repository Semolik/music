<template>
    <nuxt-link :to="link" class="clip-card" v-if="link">
        <ClipCardContent :clip="clip" :musician-info="musicianInfo" />
    </nuxt-link>
    <div class="clip-card" @click="modalOpened = true" v-else>
        <ClipCardContent :clip="clip" :musician-info="musicianInfo" />
    </div>
    <ModalDialog
        :active="modalOpened"
        @close="modalOpened = false"
        max-width="80vw"
    >
        <template #content>
            <iframe
                :src="`${YOUTUBE_EMBED_URL}/${clip.video_id}`"
                class="youtube-embed"
                width="100%"
                height="100%"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
            ></iframe>
        </template>
    </ModalDialog>
</template>
<script setup>
const { YOUTUBE_EMBED_URL } = useRuntimeConfig().public;
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

const modalOpened = ref(false);
</script>
<style lang="scss" scoped>
.youtube-embed {
    aspect-ratio: 16 / 9;
    border-radius: 10px;
}
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
