<template>
    <header>
        <router-link to="/" class="text" @click="this.$emit('reset_error')">Музыка</router-link>
        <div class="header-buttons">
            <router-link @[logined&&`mouseover`]="panelActive = true"
                :class="['header-button', 'login', { logined: logined }, { normal: !panelActive }]"
                :to="!logined ? '/login' : '/lk'">
                <div class="icon">
                    <FontAwesomeIcon icon="fa-user" v-if="logined" />
                    <FontAwesomeIcon icon="fa-right-from-bracket" v-else />
                </div>
            </router-link>
            <div :class="['account-panel', { active: panelActive }]" v-if="logined && userData"
                @[logined&&`mouseleave`]="panelActive = false">
                <div class="line">
                    <div class="info">
                        <div class="info-text">{{ fullName }}</div>
                    </div>
                </div>
                <div class="menu">
                    <router-link to="/lk" @click="clicked" class="item">Личный кабинет</router-link>
                    <div class="item" @click="clicked(logoutRequest)">Выйти из аккаунта</div>
                </div>
            </div>
        </div>
    </header>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faSun, faMoon, faBars, faRightFromBracket, faUser } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useThemeStore } from '../stores/theme';
import { useAuthStore } from '../stores/auth';
import { storeToRefs } from 'pinia';

library.add([faSun, faMoon, faBars, faRightFromBracket, faUser]);

export default {
    setup() {
        const AuthStore = useAuthStore();
        const themeStore = useThemeStore();

        const { logined, userData } = storeToRefs(AuthStore);
        const { themeName } = storeToRefs(themeStore);
        const { toggleTheme } = themeStore;
        const { logoutRequest } = AuthStore;
        return {
            themeName,
            toggleTheme,
            logined,
            userData,
            logoutRequest
        }
    },
    components: {
        FontAwesomeIcon,
    },
    emits: ['blur_content', 'hide_body_overflow'],
    data() {
        return {
            themeToggle: false,
            panelActive: false,
        }
    },
    computed: {
        fullName() {
            if (!this.userData) return
            return [this.userData.first_name, this.userData.last_name].filter(Boolean).join(' ') || this.userData.username
        }
    },
    watch: {
        logined(value) {
            console.log(value)
            if (value === false) {
                this.$router.push({ path: '/login' })
            }
        }
    },
    methods: {
        clicked(func) {
            this.panelActive = false;
            if (func) func();
        }
    }
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/helpers';

header {
    @include helpers.flex-center;
    width: 100%;
    height: var(--header-height);
    padding: 1rem;
    gap: 10px;
    z-index: 10;
    position: relative;
    margin-bottom: 10px;

    @include breakpoints.xl {
        margin: 10px 0px;
        border-radius: 20px;
    }

    transition: border-color .2s;
    background-color: var(--color-background-soft);

    .text {
        font-size: x-large;
        margin-right: auto;
        height: min-content;
        color: var(--color-header-text);
        text-decoration: none;
    }

    .account-panel {
        position: absolute;
        top: 0;
        z-index: -1;
        background-color: var(--color-background-mute-2);
        overflow: hidden;
        max-width: 0px;
        right: 0;

        @include breakpoints.xl {
            border-radius: 20px;
        }

        @include breakpoints.xl(true) {
            border-radius: 20px 0px 0px 20px;
        }

        &:where(.active, :hover) {
            min-width: 300px;
            min-height: 100%;
        }

        .line {

            height: calc(40px + 2rem);
            margin-right: calc(40px + 2rem); //Ширина кнопки + отступ хедера
            display: flex;

            .info {
                flex-grow: 1;
                padding: 10px;
                @include helpers.flex-center;

                .info-text {
                    font-size: 1.2em;
                }
            }
        }

        .menu {
            display: flex;
            flex-direction: column;

            .item {
                &:not(:last-child) {
                    border-bottom: 1px solid var(--color-background-mute);
                }

                padding: 10px;
                background-color: var(--color-background-mute-3);
                text-align: center;
                cursor: pointer;
                text-decoration: none;
                color: var(--color-text);

                &:hover {
                    background-color: var(--color-background-mute-4);
                }
            }
        }
    }


    .header-buttons {
        display: flex;
        gap: 10px;

        .header-button {
            height: 40px;
            width: 40px;
            border-radius: 50%;
            padding: 8px;
            overflow: hidden;

            .icon {
                width: 100%;
                height: 100%;

                svg {
                    color: black;
                    width: 100%;
                    height: 100%;
                }
            }

            &.login {
                background-color: var(--login-icon-color);
                position: relative;
                transition: border-radius .2s, background-color .2s;

                &:hover {
                    background-color: var(--login-icon-color-hover);
                }
            }
        }

        .themeswitch {
            position: relative;
            overflow: hidden;

            &.light {
                background-color: var(--light-theme-toggle-color);
            }

            &.dark {
                background-color: var(--dark-theme-toggle-color);

                .icons {
                    top: -100%;
                }
            }

            .icons {
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                transition: .2s top;

                .icon {
                    padding: 8px;
                }
            }
        }
    }
}
</style>