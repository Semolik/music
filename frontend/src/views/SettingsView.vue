<template>
    <div class="lk-container">
        <aside>
            <router-link class="aside-item lk-link" to="/lk">{{ lkButtonText }}</router-link>
            <router-link class="aside-item" to="/lk/public" v-if="isCustomProfileActive">Публичный профиль</router-link>
            <router-link class="aside-item" to="/lk/my-music" v-if="isMusician">Кабинет музыканта</router-link>
            <router-link class="aside-item" to="/lk/music">Моя музыка</router-link>
            <router-link class="aside-item" to="/lk/update-status" v-if="!isAdmin">Изменение статуса аккаунта
            </router-link>
            <router-link class="aside-item" to="/lk/update-status-requests" v-else>Заявки на изменение статуса
            </router-link>
            <router-link class="aside-item" to="/lk/edit-musician-section" v-if="isAdmin">Музыкальный раздел
            </router-link>
        </aside>
        <div class="active-route">
            <router-view v-slot="{ Component, route }" appear>
                <Transition name="list" mode="out-in">
                    <div :key="route.fullPath" class="transition-wrapper">
                        <component :is="Component" />
                    </div>
                </Transition>
            </router-view>
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
@use '@/assets/styles/animations';

.lk-container {
    overflow: hidden;
    display: grid;
    grid-template-columns: 270px 1fr;
    background-color: var(--color-background-mute);
    width: 100%;
    border-radius: 15px;

    @include breakpoints.lg(true) {
        grid-template-columns: 1fr;
    }

    @include breakpoints.xl(true) {
        border-radius: 0;
    }

    aside {
        padding: 10px;
        display: flex;
        flex-wrap: wrap;
        flex-direction: column;
        gap: 5px;
        height: min-content;

        @include breakpoints.lg(true) {
            grid-template-columns: 1fr;
            flex-direction: row;
        }

        .aside-item {
            flex-grow: 1;
            position: relative;
            display: flex;
            padding: 10px;
            text-decoration: none;
            overflow: hidden;
            color: var(--color-text);
            border-radius: 5px;
            isolation: isolate;

            @include breakpoints.lg(true) {
                @include helpers.flex-center;


            }

            &.lk-link.router-link-exact-active,
            &.router-link-active:not(.lk-link) {
                background-color: var(--color-background-mute-3);
            }

            &.lk-link:not(.lk-link.router-link-exact-active):hover,
            &:hover:not(.router-link-active) {
                background-color: var(--color-background-mute-2);
            }
        }
    }

    .active-route {
        background-color: var(--color-background-mute-2);
        padding: 10px;
        height: 100%;
        @include animations.list;
    }
}
</style>