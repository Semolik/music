<template>
    <div class="app-player-wrapper">
        <div class="app-player">
            <div class="player-buttons">
                <div class="player-button">
                    <FontAwesomeIcon icon="fa-backward" />
                </div>
                <div class="player-button">
                    <FontAwesomeIcon icon="fa-play" />
                </div>
                <div class="player-button">
                    <FontAwesomeIcon icon="fa-forward" />
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import { usePlayerStore } from '../stores/player';
import { storeToRefs } from 'pinia';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlay, faForward, faBackward } from '@fortawesome/free-solid-svg-icons';
library.add(faPlay, faForward, faBackward);
export default {
    setup() {
        const { } = storeToRefs(usePlayerStore());
        const { } = usePlayerStore();
        return {};
    },
    components: { FontAwesomeIcon }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';

.app-player-wrapper {
    position: absolute;
    padding: 0px 5px;
    bottom: 10px;
    display: flex;
    width: min(1200px, 100%);

    .app-player {
        background-color: var(--color-background-mute);
        padding: 10px;
        width: 100%;
        border-radius: 20px;

        .player-buttons {
            display: flex;
            gap: 5px;

            .player-button {
                @include helpers.flex-center;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background-color: var(--color-background-mute-2);
                cursor: pointer;

                svg {
                    color: var(--color-header-text);
                }

                &:hover {
                    background-color: var(--color-background-mute-3);
                }
            }
        }
    }
}
</style>