<template>
    <ShareModal
        :active="active"
        text="Поделиться треком"
        :link="trackLink"
        @update:active="emit('update:active', $event)"
    >
        <template #content>
            <ShareSocial :link="trackLink" />
            <AppButtonCopy :value="trackLink" />
        </template>
    </ShareModal>
</template>

<script setup>
const { active, track } = defineProps({
    active: {
        type: Boolean,
        default: false,
    },
    track: {
        type: Object,
        default: null,
    },
});
const trackLink = ref("");
onMounted(() => {
    trackLink.value = window.location.origin + "/track/" + track.id;
});
const emit = defineEmits(["update:active"]);
</script>
