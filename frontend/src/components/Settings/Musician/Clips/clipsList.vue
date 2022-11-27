<template>
    <div class="clips">
        <ClipsListItem @clip-click="$emit('clip-click', $event)" :clip="clip" :base-url="baseUrl"
            v-for="clip in clips" />
        <div class="whach-more-link-container" v-if="watchMoreLink">
            <router-link class="whach-more-link" :to="watchMoreLink">
                <div class="icon">
                    <FontAwesomeIcon icon="fa-ellipsis" />
                </div>
            </router-link>
        </div>
    </div>
</template>
<script>
import ClipsListItem from './clipsListItem.vue';
import { faEllipsis } from '@fortawesome/free-solid-svg-icons';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faEllipsis)
export default {
    props: {
        clips: Array,
        baseUrl: String,
        watchMoreLink: String
    },
    components: { ClipsListItem, FontAwesomeIcon },
}
</script>
<style lang="scss" scoped>
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';

.clips {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;

    @include breakpoints.lg(true) {
        grid-template-columns: repeat(3, 1fr);
    }

    @include breakpoints.md(true) {
        grid-template-columns: repeat(2, 1fr);
    }

    @include breakpoints.sm(true) {
        grid-template-columns: 1fr;
    }

    .whach-more-link-container {
        display: flex;
        flex-direction: column;

        .whach-more-link {

            aspect-ratio: 16 / 9;
            overflow: hidden;
            border-radius: 10px;
            background-color: var(--color-background-mute-2);
            position: relative;
            @include helpers.flex-center;

            &:hover {
                &::after {
                    opacity: 1;
                }
            }

            .icon {
                width: 60px;
                height: 60px;
                background-color: var(--color-background-mute-3);
                @include helpers.flex-center;
                border-radius: 50%;

                svg {
                    width: 30px;
                    height: 30px;
                    color: var(--color-text);
                }
            }

            &::after {
                content: '';
                background-color: rgba($color: white, $alpha: 0.07);
                position: absolute;
                inset: 0;
                opacity: 0;
                transition: opacity .2s;
            }
        }
    }
}
</style>