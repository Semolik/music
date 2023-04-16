<template>
    <div class="cards-container" v-auto-animate>
        <slot />
    </div>
</template>
<style lang="scss" scoped>
.cards-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
    gap: 10px;
    @include lg(true) {
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    }
    grid-template-rows: min-content;
}
</style>
