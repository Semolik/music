<template>
    <div class="info-items">
        <InfoItem :item="item" v-for="item in items" />
    </div>
</template>
<script setup>
const { items } = defineProps({
    items: Array,
});
</script>
<style lang="scss" scoped>
.info-items {
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>
