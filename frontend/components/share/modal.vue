<template>
    <ModalDialog
        :active="active"
        :head-text="text"
        close-on-esckey
        @close="emit('update:active', false)"
    >
        <template #content>
            <ShareSocial :link="linkLocal" />
            <AppButtonCopy :value="linkLocal" />
        </template>
    </ModalDialog>
</template>

<script setup>
const { active, link, text, addHost } = defineProps({
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
    addHost: {
        type: Boolean,
        default: false,
    },
});
const linkLocal = ref(link);
if (addHost) {
    onMounted(() => {
        linkLocal.value = `${window.location.origin}${link}`;
    });
}
const emit = defineEmits(["update:active"]);
</script>
