<template>
    <ModalDialog
        :active="active"
        head-text="Поделиться треком"
        close-on-esckey
        @close="emit('update:active', false)"
    >
        <template #content>
            <ShareSocial :link="trackLink" />
            <AppButtonCopy :value="trackLink" />
        </template>
    </ModalDialog>
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
const trackLink = computed(() => {
    return window.location.origin + "/track/" + track.id;
});
const emit = defineEmits(["update:active"]);
</script>
