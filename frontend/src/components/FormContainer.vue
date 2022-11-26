<template>
    <div :class="['container',{center: center}]" :style="{width: `min(${width}px, 100%)`}">
        <slot></slot>
    </div>
</template>
<script>
export default {
    props: {
        formWidth: Number,
        center: Boolean
    },
    data() {
        return {
            defaultWidth: 300
        }
    },
    computed: {
        width() {
            return this.formWidth || this.defaultWidth
        }
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/helpers';

.container {
    margin: auto;
    display: flex;
    flex-direction: column;
    gap: 10px;
    background-color: var(--color-background-mute);
    padding: 10px;
    border-radius: 15px;

    &.center {
        @include helpers.flex-center;
    }
}
</style>