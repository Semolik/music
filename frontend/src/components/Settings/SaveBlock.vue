<template>
    <div class="buttons custom">
        <slot></slot>
        <div :class="['button', 'save', { active: active }, { wrong: wrong }]">
            <FontAwesomeIcon icon="fa-floppy-disk" />
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faFloppyDisk } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faFloppyDisk);
export default {
    props: {
        active: Boolean,
        wrong: Boolean,
    },
    components: {
        FontAwesomeIcon
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/breakpoints';
@use '@/assets/styles/components';


.buttons {
    margin-top: auto;
    display: flex;
    gap: 5px;
    justify-content: right;

    &.custom {
        .button {

            width: 40px;
            height: 40px;
            border-radius: 10px;
            padding: 5px;
            cursor: auto;
            @include helpers.flex-center;
            background-color: var(--color-background-mute-4);

        }
    }

    .button {
        @include components.button;

        @include breakpoints.xl(true) {
            width: 100%;
        }

        &.save {

            &.wrong {
                background-color: var(--red-0);
                cursor: not-allowed;
            }

            &.active {
                background-color: var(--purple-1);
                cursor: pointer;
            }
        }

        &.delete {

            &:hover {
                cursor: pointer;
                background-color: var(--red-0);
            }
        }
    }
}
</style>