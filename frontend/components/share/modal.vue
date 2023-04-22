<template>
    <ModalDialog
        :active="active"
        :head-text="text"
        close-on-esckey
        @close="emit('update:active', false)"
    >
        <template #content>
            <ShareSocial :link="link" />
            <AppButtonCopy :value="link" />
        </template>
    </ModalDialog>
</template>

<script setup>
defineProps({
    active: {
        type: Boolean,
        default: false,
    },
    link: {
        type: String,
        default: null,
    },
    text: {
        type: String,
        default: null,
    },
});

const emit = defineEmits(["update:active"]);
</script>
