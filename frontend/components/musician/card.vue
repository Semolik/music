<template>
    <div class="musician-card">
        <musician-avatar :avatar="musician.picture" />
        <div class="musician-card-name">{{ musician.name }}</div>
    </div>
</template>
<script setup>
const { musician } = defineProps({
    musician: {
        type: Object,
        required: true,
    },
});
</script>
<style lang="scss">
.musician-card {
    @include flex-center;
    flex-direction: column;
    height: 100%;
    width: 100%;
    gap: 5px;
}
</style>
