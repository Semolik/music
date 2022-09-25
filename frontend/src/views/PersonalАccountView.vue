<template>
    <div class="lk-container">
        <aside>
            <router-link class="item" to="/lk">Профиль</router-link>
            <div class="item">Профиль</div>
            <div class="item">Профиль</div>
            <div class="item">Профиль</div>
        </aside>
        <div class="active-route">
            <router-view></router-view>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.lk-container {
    display: grid;
    grid-template-columns: 270px 1fr;
    background-color: var(--color-background-mute);
    padding: 10px;
    width: 100%;
    border-radius: 20px;
    gap: 10px;

    aside {
        background-color: var(--color-background-mute-2);
        border-radius: 10px;
        padding: 5px;
        display: grid;
        grid-auto-rows: min-content;
        gap: 5px;

        .item {
            position: relative;
            display: flex;
            padding: 10px;
            text-decoration: none;
            overflow: hidden;
            color: var(--color-text);
            border-radius: 5px;
            background-color: var(--color-background-mute-3);

            &:hover {
                background-color: var(--color-background-mute-4);
            }

            &::after {
                content: '';
                height: 100%;
                position: absolute;
                right: 0;
                top: 0;
                background-color: var(--purple-1);
                width: 3px;
                opacity: 0;
                transition: opacity .2s;
            }

            &.router-link-active::after {
                opacity: 1;
            }
        }
    }

    .active-route {
        background-color: var(--color-background-mute-2);
        border-radius: 10px;
        padding: 10px;
    }
}
</style>