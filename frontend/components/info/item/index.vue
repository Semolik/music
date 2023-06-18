<template>
    <nuxt-link
        :class="['info-item', { vertical: item.vertical }]"
        :to="item.to"
        v-if="item.to"
    >
        <InfoItemContent :item="item" />
    </nuxt-link>
    <div :class="['info-item', { vertical: item.vertical }]" v-else>
        <InfoItemContent :item="item" />
    </div>
</template>
<script setup>
const { item } = defineProps({
    item: Object,
});
</script>
<style lang="scss" scoped>
a.info-item {
    @include lg {
        &:hover {
            .value {
                background-color: $senary-bg;
            }

            .title {
                background-color: $quinary-bg;
            }

            .go-to {
                background-color: $quaternary-bg-2;
                color: $primary-text;
                svg {
                    color: $primary-text;
                }
            }
        }
    }
}
.info-item {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    width: 100%;
    overflow: hidden;
    border-radius: 10px;
    border: 1px solid $quaternary-bg;

    &.vertical {
        grid-template-columns: 1fr;
    }
}
</style>
