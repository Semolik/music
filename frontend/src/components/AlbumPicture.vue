<template>
    <div :class="['picture', { hoverable: !offHover }]">
        <img :src="src" alt="" v-if="src">
        <div class="empty-picture" v-else>
            <FontAwesomeIcon icon="fa-music" />
        </div>
        <div class="icon" v-if="editIcon">
            <FontAwesomeIcon icon="fa-pen" />
        </div>
        <div :class="['play-icon', { active: playIcon }]">
            <FontAwesomeIcon icon="fa-play" />
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faMusic, faPen, faPlay } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faMusic, faPen, faPlay);
export default {
    props: {
        src: String,
        offHover: Boolean,
        editIcon: Boolean,
        isTrack: Boolean,
        playIcon: Boolean
    },
    components: {
        FontAwesomeIcon
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.picture {
    aspect-ratio: 1;
    border-radius: var(--picture-border-radius, 10px);
    width: 100%;
    overflow: hidden;
    isolation: isolate;
    position: relative;

    .play-icon {
        &.active {
            opacity: 1;
        }

        transition: opacity .2s;
        opacity: 0;
        position: absolute;
        inset: 0;
        @include helpers.flex-center;
        color: var(--yellow);
        background-color: rgba($color: #000000, $alpha: 0.4);

        svg {
            width: var(--svg-size, 24px);
            height: var(--svg-size, 24px);
        }
    }

    &.hoverable:hover {
        .empty-picture {
            background-color: var(--hover-picture-color, var(--color-background-mute-6));
        }

        &:has(img) {
            &::after {
                opacity: 1;
            }
        }

        .icon {
            opacity: 1;
        }
    }



    &.hoverable {

        .icon,
        &::after {
            content: '';
            position: absolute;
            transition: .2s opacity;
            inset: 0;
            opacity: 0;
            z-index: 2;
            background-color: rgba($color: white, $alpha: 0.15);
        }

        .icon {
            @include helpers.flex-center;
            color: var(--color-text-rev);
            z-index: 3;
            cursor: pointer;

            svg {
                width: var(--svg-size, 24px);
                height: var(--svg-size, 24px);
            }
        }
    }

    img {
        object-fit: cover;
        width: 100%;
        height: 100%;
        position: relative;
        isolation: isolate;
    }

    .empty-picture {
        background-color: var(--picture-color, var(--color-background-mute-3));
        width: 100%;
        height: 100%;
        @include helpers.flex-center;

        svg {
            height: var(--svg-size, 20%);
            width: var(--svg-size, 20%);
            color: var(--svg-color);
        }
    }
}
</style>
