<template>
    <router-link class="album" :to="`albums/${albumInfo.id}`">
        <dib class="picture">
            <img :src="albumInfo.picture" alt="" v-if="albumInfo.picture">
            <div class="empty-picture" v-else>
                <FontAwesomeIcon icon="fa-music" />
            </div>
        </dib>
        <div class="name">{{ albumInfo.name }}</div>
    </router-link>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faMusic } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faMusic);
export default {
    props: {
        albumInfo: Object
    },
    components: {
        FontAwesomeIcon
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.album {
    display: flex;
    flex-direction: column;
    cursor: pointer;
    gap: 5px;
    text-align: center;
    color: var(--color-text);
    text-decoration: none;

    .name {
        text-align: center;
    }

    .picture {
        aspect-ratio: 1;
        border-radius: 10px;
        width: 100%;
        overflow: hidden;
        isolation: isolate;
        position: relative;

        &:hover {
            .empty-picture {
                background-color: var(--color-background-mute-6);
            }

            &:has(img) {
                &::after {
                    opacity: 1;
                }
            }
        }



        &::after {
            content: '';
            position: absolute;
            transition: .2s opacity;
            inset: 0;
            opacity: 0;
            z-index: 2;
            background-color: rgba($color: white, $alpha: 0.15);
        }

        img {
            object-fit: cover;
            width: 100%;
            height: 100%;
            position: relative;
            isolation: isolate;
        }

        .empty-picture {
            background-color: var(--color-background-mute-3);
            width: 100%;
            height: 100%;
            @include helpers.flex-center;

            svg {
                height: 20%;
                width: 20%;

            }
        }
    }

}
</style>