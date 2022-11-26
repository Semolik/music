<template>
    <div class="musician-container">
        <div class="musician-container-head">
            <div class="head-bg">
                <img :src="publicProfileData.picture" v-if="publicProfileData.picture">
            </div>
            <div :class="['musician-container-picture', { empty: !publicProfileData.picture }]">
                <img :src="publicProfileData.picture" alt="" v-if="publicProfileData.picture">
                <FontAwesomeIcon icon="fa-image" />
            </div>
            <div class="social-links-container">
                <div class="social-links">
                    <a class="link" v-if="vkLink" :href="vkLink" target="_blank">
                        <FontAwesomeIcon :icon="['fab', 'vk']" />
                    </a>
                </div>
            </div>
        </div>
        <div class="musician-container-content">
            sdasd
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faImage } from '@fortawesome/free-solid-svg-icons';
import { faYoutube, faTelegram, faVk } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { useToast } from 'vue-toastification';
import { HTTP } from '../http-common.vue';
library.add(faImage, faYoutube, faTelegram, faVk);
export default {
    props: {
        id: String,
    },
    async setup(props) {
        const toast = useToast();
        const response = await HTTP.get("public-profile", { params: { profile_id: props.id } });
        const publicProfileData = response.data;
        const { name } = publicProfileData;
        document.title = name;
        return { toast, publicProfileData };
    },
    components: { FontAwesomeIcon },
    computed: {
        vkLink() {
            return this.publicProfileData.links.vk
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.musician-container {
    background-color: var(--color-background-soft);
    width: 100%;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    overflow: hidden;

    .musician-container-head {
        grid-template-columns: 210px 1fr;
        display: grid;
        position: relative;
        isolation: isolate;
        overflow: hidden;
        padding: 10px;

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

        .social-links-container {
            display: flex;
            justify-content: right;

            .social-links {
                display: flex;
                height: min-content;

                .link {
                    background-color: var(--color-background-mute-2);
                    height: 40px;
                    width: 40px;
                    @include helpers.flex-center;
                    border-radius: 10px;
                    cursor: pointer;

                    &:hover {
                        background-color: var(--color-background-mute-3);
                    }

                    svg {
                        height: 20px;
                        width: 20px;
                        color: var(--color-text);
                    }
                }
            }
        }
    }

    .musician-container-content {
        padding: 10px;
    }
}
</style>