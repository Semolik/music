<template>
    <nuxt-link class="info-line-item" :to="item.link" v-if="item.link">
        <content :item="item" />
    </nuxt-link>
    <div class="info-line-item" v-else>
        <content :item="item" />
    </div>
</template>
<script setup>
const { item } = defineProps({
    item: {
        type: Object,
        required: true,
    },
});
</script>
<style lang="scss" scoped>
.info-line-item {
    display: flex;
    align-items: center;
    gap: 5px;
    color: $secondary-text;
}
</style>
