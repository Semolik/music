<template>
    <router-link class="album" :to="`/lk/my-music/albums/${albumInfo.id}`">
        <div class="picture">
            <img :src="albumInfo.picture" alt="" v-if="albumInfo.picture">
            <div class="empty-picture" v-else>
                <FontAwesomeIcon icon="fa-music" />
            </div>
        </div>
        <div class="name">{{ albumInfo.name }}</div>
        <div class="year">{{ albumInfo.year }}</div>
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
    color: var(--color-text);
    text-decoration: none;
    text-align: center;
    
    .picture {
        aspect-ratio: 1;
        border-radius: 10px;
        width: 100%;
        overflow: hidden;
        isolation: isolate;
        position: relative;
        margin-bottom: 5px;

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
    .name {
        font-weight: 600;
        padding-left: 10px;
        
    }
    .year {
        color: var(--vt-c-white-150);
        font-size: 0.9em;
    }

}
</style>