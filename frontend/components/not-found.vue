<template>
    <div class="not-found">
        {{ displayedMessage }}
    </div>
</template>
<script setup>
const props = defineProps({
    text: {
        type: String,
        default: null,
    },
});
const displayedMessage = computed(() => {
    if (props.text === null) return "По вашему запросу ничего не найдено";
    return props.text;
});
</script>
<style lang="scss" scoped>
.not-found {
    @include flex-center;
    color: $secondary-text;
    height: 100%;
}
</style>
