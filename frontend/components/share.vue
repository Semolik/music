<template>
    <ModalDialog
        :active="active"
        head-text="Поделиться"
        close-on-esckey
        @close="emit('update:active', false)"
    >
    </ModalDialog>
</template>

<script setup>
const { active } = defineProps({
    active: {
        type: Boolean,
        default: false,
    },
    link: {
        type: String,
        default: "",
    },
});
const emit = defineEmits(["update:active"]);
</script>
