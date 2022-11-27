<template>
    <div class="musician-container">
        <div class="musician-container-head">
            <div class="head-bg">
                <img :src="publicProfileData.picture" v-if="publicProfileData.picture">
            </div>
            <div :class="['musician-container-picture', { empty: !publicProfileData.picture }]">
                <img :src="publicProfileData.picture" alt="" v-if="publicProfileData.picture">
                <FontAwesomeIcon icon="fa-user" />
            </div>
            <div class="info">
                <div class="social-links-container">
                    <div class="social-links">
                        <a class="link" v-if="vkLink" :href="vkLink" target="_blank">
                            <FontAwesomeIcon :icon="['fab', 'vk']" />
                        </a>
                        <a class="link" v-if="youtubeLink" :href="youtubeLink" target="_blank">
                            <FontAwesomeIcon :icon="['fab', 'youtube']" />
                        </a>
                        <a class="link" v-if="telegramLink" :href="telegramLink" target="_blank">
                            <FontAwesomeIcon :icon="['fab', 'telegram']" />
                        </a>
                    </div>
                </div>
                <div class="name">{{ publicProfileData.name }}</div>
                <div class="social-links-container">
                    <div class="social-links">
                        <div :class="['link', 'liked', { active: liked }]" @click="toggleLike">
                            <FontAwesomeIcon icon="fa-heart" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="musician-container-content">
            <router-view></router-view>
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import { faYoutube, faTelegram, faVk } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useToast } from 'vue-toastification';
import { HTTP } from '../http-common.vue';

library.add(faUser, faYoutube, faTelegram, faVk);

export default {
    props: {
        id: String,
    },
    async setup(props) {
        const toast = useToast();
        const response = await HTTP.get("musician/", { params: { profile_id: props.id } });
        const publicProfileData = response.data;

        return { toast, publicProfileData };
    },
    provide() {
        return {
            publicProfileData: this.publicProfileData
        }
    },
    data() {
        return {
            liked: this.publicProfileData.liked,
        }
    },
    components: { FontAwesomeIcon },
    computed: {
        vkLink() {
            return this.publicProfileData.links.vk
        },
        youtubeLink() {
            return this.publicProfileData.links.youtube
        },
        telegramLink() {
            return this.publicProfileData.links.telegram
        }
    },
    methods: {
        async toggleLike() {
            const { data: { liked } } = await HTTP.post("musician/like", null, { params: { profile_id: this.id } });
            this.liked = liked;
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';

.musician-container {
    background-color: var(--color-background-soft);
    width: 100%;

    @include breakpoints.xl {
        border-radius: 15px;
    }

    display: flex;
    flex-direction: column;
    overflow: hidden;

    .musician-container-head {
        grid-template-columns: 210px 1fr;
        display: grid;
        position: relative;
        isolation: isolate;
        overflow: hidden;
        gap: 10px;
        padding: 10px;
        @include breakpoints.sm(true) {
            grid-template-columns:  1fr;
        }

        .head-bg {
            position: absolute;
            inset: 0;
            width: 100%;
            filter: blur(10px);
            z-index: -1;

            &::after {
                content: '';
                position: absolute;
                inset: 0;
                background-color: rgba($color: #000000, $alpha: 0.2);
            }

            img {
                object-fit: cover;
                width: 100%;
                height: 100%;
            }
        }

        .musician-container-picture {
            aspect-ratio: 1;
            border-radius: 10px;
            width: 100%;
            overflow: hidden;
            position: relative;

            &.empty {
                background-color: var(--color-background-mute);
                @include helpers.flex-center;

                svg {
                    height: 60px;
                    width: 60px;
                    color: var(--color-header-text);
                }
            }

            img {
                object-fit: cover;
                width: 100%;
                height: 100%;
            }
        }

        .info {
            display: flex;
            flex-direction: column;
            gap: 10px;

            .name {
                font-size: 40px;
                text-align: center;
                @include helpers.flex-center;
                flex-grow: 1;
            }

            .social-links-container {
                display: flex;
                justify-content: right;

                .social-links {
                    display: flex;
                    height: min-content;
                    gap: 5px;

                    .link {
                        background-color: var(--color-background-mute-2);
                        height: 40px;
                        width: 40px;
                        @include helpers.flex-center;
                        border-radius: 10px;
                        cursor: pointer;

                        &.liked.active svg {
                            color: var(--red);
                        }

                        &.favotite-button {
                            position: absolute;
                            bottom: 10px;
                            right: 10px;
                        }

                        &:hover {
                            background-color: var(--color-background-mute-3);
                        }

                        svg {
                            height: 18px;
                            width: 18px;
                            color: var(--color-text);
                        }
                    }
                }
            }
        }
    }

    .musician-container-content {
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 20px;

        .headline {
            font-size: 22px;
            color: var(--color-header-text);
            &.center {
                text-align: center;
            }
        }

    }
}
</style>