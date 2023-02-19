<template>
    <card
        :text="musician.name"
        :picture="musician.picture"
        icon="material-symbols:person-rounded"
    />
</template>
<script setup>
const { musician } = defineProps({
    musician: {
        type: Object,
        required: true,
    },
});
</script>
