<template>
    <ModalDialog
        :active="modalOpened"
        @close="emit('update:modalOpened', false)"
        max-width="70vw"
        max-height="90vh"
        close-on-esckey
    >
        <template #content>
            <iframe
                :src="`${YOUTUBE_EMBED_URL}/${clip.video_id}`"
                class="youtube-embed"
                width="100%"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
            ></iframe>
            <TrackCard
                :track="clip.track"
                v-if="clip.track"
                @update:track="emit('update:clip', { ...clip, track: $event })"
            />
        </template>
    </ModalDialog>
</template>
<script setup>
const { YOUTUBE_EMBED_URL } = useRuntimeConfig().public;
const { clip, modalOpened } = defineProps({
    clip: {
        type: Object,
        required: true,
    },
    modalOpened: {
        type: Boolean,
        required: false,
        default: false,
    },
});
const emit = defineEmits(["update:modalOpened", "update:clip"]);
</script>
<style scoped>
.youtube-embed {
    aspect-ratio: 16 / 9;
    border-radius: 10px;
}
</style>
