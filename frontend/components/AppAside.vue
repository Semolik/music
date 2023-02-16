<template>
    <aside>
        <div class="selections">
            <NuxtLink to="/" class="selection">
                <Icon name="iconoir:home" />
                <span>Главная</span>
            </NuxtLink>
            <NuxtLink to="/history" class="selection">
                <Icon name="codicon:history" />
                <span>История прослушивания</span>
            </NuxtLink>
            <NuxtLink to="/history" class="selection">
                <Icon name="iconoir:heart" />
                <span>Любимые треки</span>
            </NuxtLink>
        </div>
        <div class="account-info">
            <NuxtLink to="/history" class="selection">
                <Icon name="iconoir:log-in" />
                <span>Войти в аккаунт</span>
            </NuxtLink>
        </div>
    </aside>
</template>
<style lang="scss">
aside {
    background-color: $secondary-bg;
    padding: 20px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    a.selection {
        @include flex-center;
        text-decoration: none;
        gap: 10px;
        padding: 13px;
        border-radius: 5px;
        color: $secondary-text;
        cursor: pointer;
        @include sm(true) {
            &:not(.mobile) {
                display: none;
            }
            &.menu {
                display: flex;
            }
        }

        &.router-link-active {
            @include sm {
                background-color: $tertiary-bg;
            }
            span,
            svg {
                color: $primary-text;
            }
            svg {
                &.default {
                    display: none;
                }
            }
        }
        &:not(.router-link-active) {
            span,
            svg {
                color: $secondary-text;
            }
            svg {
                &.active {
                    display: none;
                }
            }
        }
        @include sm {
            &:hover {
                background-color: $tertiary-bg;
            }
            &.menu {
                display: none;
            }
        }
        svg {
            width: 25px;
            height: 25px;
            color: $primary-text;
            transition: color 0s;
        }

        span {
            flex-grow: 1;
            display: flex;
            align-items: center;
            margin-right: 20px;
            white-space: nowrap;
        }
    }
    .selections {
        display: flex;
        flex-direction: column;
        gap: 10px;
        flex-grow: 1;
    }
    .account-info {
        display: flex;
        flex-direction: column;
        a.selection {
            // background-color: $tertiary-bg;
        }
    }
}
</style>
