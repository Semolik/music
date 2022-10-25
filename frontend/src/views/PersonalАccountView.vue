<template>
    <div class="lk-container">
        <aside>
            <router-link class="item" to="/lk">{{ lkButtonText }}</router-link>
            <router-link class="item" to="/lk/public" v-if="isCustomProfileActive">Публичный профиль</router-link>
            <router-link class="item" to="/lk/music">Моя музыка</router-link>
            <router-link class="item" to="/lk/update-status" v-if="!isAdmin">Изменение статуса аккаунта</router-link>
            <router-link class="item" to="/lk/update-status-requests" v-else>Заявки на изменение статуса</router-link>
            <router-link class="item" to="/lk/my-music" v-if="isMusician">Кабинет музыканта</router-link>
        </aside>
        <div class="active-route">
            <router-view></router-view>
        </div>
    </div>
</template>
<script>
import { storeToRefs } from 'pinia';
import { useAuthStore } from '../stores/auth';
export default {
    setup() {
        const { isAdmin, isMusician, isUser, isRadioStation } = storeToRefs(useAuthStore());
        return {
            isAdmin, isMusician, isUser, isRadioStation
        }
    },
    computed: {
        lkButtonText() {
            if (this.isCustomProfileActive) {
                return 'Личный профиль'
            }
            return 'Профиль'
        },
        isCustomProfileActive() {
            return this.isMusician || this.isRadioStation
        }
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/helpers';

.lk-container {
    display: grid;
    grid-template-columns: 270px 1fr;
    background-color: var(--color-background-mute);
    padding: 10px;
    width: 100%;
    border-radius: 30px;
    gap: 10px;

    @include breakpoints.lg(true) {
        grid-template-columns: 1fr;
    }

    aside {
        background-color: var(--color-background-mute-2);
        border-radius: 20px;
        padding: 5px;
        display: flex;
        flex-wrap: wrap;
        flex-direction: column;
        gap: 5px;
        height: min-content;

        @include breakpoints.lg(true) {
            grid-template-columns: 1fr;
            flex-direction: row;
        }

        .item {
            flex-grow: 1;
            position: relative;
            display: flex;
            padding: 10px;
            text-decoration: none;
            overflow: hidden;
            color: var(--color-text);
            border-radius: 15px;
            background-color: var(--color-background-mute-3);

            @include breakpoints.lg(true) {
                @include helpers.flex-center;

                &.router-link-exact-active {
                    background-color: var(--purple);
                }
            }

            @include breakpoints.lg {
                &.router-link-exact-active::after {
                    opacity: 1;
                }
            }

            &:not(.router-link-exact-active):hover {
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

        }
    }

    .active-route {
        background-color: var(--color-background-mute-2);
        border-radius: 20px;
        padding: 10px;
    }
}
</style>