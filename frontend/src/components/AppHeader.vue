<template>
    <header>
        <router-link to="/" class="text" @click="this.$emit('reset_error')">Музыка</router-link>
        <div class="buttons">
            <div :class="['themeswitch', 'button', themeName]" @click="toggleTheme"
                v-if="logined ? !panelActive : true">
                <div class="icons">
                    <div class="icon">
                        <FontAwesomeIcon icon="fa-sun" />
                    </div>
                    <div class="icon">
                        <FontAwesomeIcon icon="fa-moon" />
                    </div>
                </div>
            </div>
            <router-link @[logined&&`mouseover`]="panelActive = true"
                :class="['button', 'login', {logined: logined},{normal: !panelActive}]" :to="!logined ? 'login': 'lk'">
                <div class="icon">
                    <FontAwesomeIcon icon="fa-user" v-if="logined" />
                    <FontAwesomeIcon icon="fa-right-from-bracket" v-else />
                </div>
            </router-link>
            <div :class="['account-panel', {active: panelActive}]" v-if="logined"
                @[logined&&`mouseleave`]="panelActive = false">
                <div class="line">
                    <div class="info">
                        <div class="info-text">Сладкопар Жижедуй</div>
                    </div>
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
        const { logined } = storeToRefs(useAuthStore());
        const themeStore = useThemeStore();
        const { themeName } = storeToRefs(themeStore);
        const { toggleTheme } = themeStore;
        return {
            themeName,
            toggleTheme,
            logined
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
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/themes';
@use '@/assets/styles/helpers';

header {
    @include helpers.flex-center;
    width: 100%;
    height: var(--header-height);
    padding: 1rem;
    gap: 10px;
    z-index: 10;
    position: relative;

    @include breakpoints.xl {
        margin: 10px 0px;
        border-radius: 20px;
    }

    transition: border-color .2s;

    @include themes.dark {
        background-color: var(--color-background-soft);
    }

    @include themes.light {
        background-color: var(--color-background-mute);
    }

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
            // padding: 10px;
        }

        .line {
            height: calc(40px + 2rem);
            margin-right: calc(40px + 2rem); //Ширина кнопки + отступ хедера
            display: flex;

            .info {
                background-color: red;
                flex-grow: 1;
                padding: 10px;
                @include helpers.flex-center;

                .info-text {
                    font-size: 1.2em;
                }
            }
        }
    }


    .buttons {
        display: flex;
        gap: 10px;

        .button {
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

                &.logined {
                    &:not(.normal) {
                        background-color: transparent;
                        border-radius: 0px;

                        &:hover {
                            background-color: transparent;
                        }
                    }
                }
            }
        }

        .nav-toggle {
            background-color: var(--nav-toggle-color);
            position: relative;

            &.active {
                .icon {
                    &.on {
                        opacity: 1;
                        transform: rotate(0deg);
                    }

                    &.off {
                        opacity: 0;
                        transform: rotate(90deg);
                    }
                }
            }

            .icon {
                &.on {
                    opacity: 0;
                    transform: rotate(90deg);
                }

                &.off {
                    opacity: 1;
                    transform: rotate(0deg);
                }

                transition: opacity .2s,
                transform .2s;
                position: absolute;
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