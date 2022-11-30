<template>
    <div class="buttons custom">
        <slot></slot>
        <div class="button delete" @click="$emit('delete')" v-if="deleteButton">
            <FontAwesomeIcon icon="fa-trash" />
        </div>
        <div :class="['button', 'save', { active: active }, { wrong: wrong }]" @click="$emit('save')">
            <FontAwesomeIcon icon="fa-floppy-disk" />
        </div>
    </div>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faFloppyDisk,faTrash } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faFloppyDisk,faTrash);
export default {
    props: {
        active: Boolean,
        wrong: Boolean,
        deleteButton: Boolean,
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

                &:hover {
                    background-color: var(--red-0);
                }
            }

            &.active {
                background-color: var(--purple-1);
                cursor: pointer;

                &:hover {
                    background-color: var(--purple-1);
                }
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