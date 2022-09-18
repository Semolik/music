<template>
    <header :class="{ active: nav_opened }">
        <router-link to="/" class="text" @click="this.$emit('reset_error')">Музыка</router-link>
        <div class="buttons">
            <div :class="['themeswitch', 'button', themeName]" @click="toggleTheme">
                <div class="icons">
                    <div class="icon">
                        <FontAwesomeIcon icon="fa-sun" />
                    </div>
                    <div class="icon">
                        <FontAwesomeIcon icon="fa-moon" />
                    </div>
                </div>
            </div>
            <router-link class="button login" to="/login">
                <div class="icon">
                    <FontAwesomeIcon icon="fa-right-from-bracket" />
                </div>
            </router-link>
        </div>
    </header>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faSun, faMoon, faBars, faRightFromBracket } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useThemeStore } from '../stores/theme';
import { storeToRefs } from 'pinia';

library.add([faSun, faMoon, faBars, faRightFromBracket]);

export default {
    setup() {
        const themeStore = useThemeStore();
        const { themeName } = storeToRefs(themeStore);
        const { toggleTheme } = themeStore;
        return {
            themeName,
            toggleTheme,
        }
    },
    components: {
        FontAwesomeIcon,
    },
    emits: ['blur_content', 'hide_body_overflow'],
    methods: {
        toggleNav() {
            this.nav_opened = !this.nav_opened;
            this.$emit('blur_content', this.nav_opened);
        }
    },
    data() {
        return {
            themeToggle: false,
            nav_opened: false,
            links: [
                {
                    'name': 'Образовательный портал',
                    'url': 'https://portal.edu.asu.ru/my'
                },
                {
                    'name': 'Сайт университета',
                    'url': 'https://asu.ru'
                },
                {
                    'name': 'Автор',
                    'url': 'https://vk.com/id612410511'
                },
            ],
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

    .buttons {
        display: flex;
        gap: 10px;

        .button {
            height: 40px;
            width: 40px;
            border-radius: 50%;

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

                &:hover {
                    background-color: var(--login-icon-color-hover);
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