<template>
    <div class="default-layout">
        <AppAside />
        <div class="content-container">
            <AppHeader />
            <slot />
        </div>
    </div>
</template>
<style lang="scss">
.default-layout {
    display: grid;
    grid-template-columns: min-content 1fr;
    height: 100%;
    .content-container {
        display: flex;
        flex-direction: column;
    }
}
</style>
