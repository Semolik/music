<template>
    <Teleport to="#modal">
        <Transition name="modal">
            <div class="modal-bg" v-if="active" @click.self="closeModal">
                <div class="modal" :style="{ '--modal-max-width': maxWidth, '--content-padding': padding }">
                    <div class="headline">
                        <div class="text">{{ headline }}</div>
                        <div class="close-button" @click="closeModal">
                            <FontAwesomeIcon icon="fa-x" />
                        </div>
                    </div>
                    <div class="modal-content">
                        {{ text }}
                        <slot></slot>
                    </div>
                    <div class="modal-buttons">
                        <div :class="['button', { loading: yesLoading }]" v-if="yesButton" @click="$emit('yes')">
                            <span v-if="!yesLoading">Да</span>
                            <FontAwesomeIcon icon="fa-spinner" v-else />
                        </div>
                        <div class="button" v-if="noButton" @click="$emit('no')">Нет</div>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faX, faSpinner } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faX, faSpinner);

export default {
    props: {
        active: Boolean,
        headline: String,
        text: String,
        yesButton: Boolean,
        yesLoading: Boolean,
        noButton: Boolean,
        maxWidth: String,
        padding: {
            type: String,
            default: '10px',
        },
    },
    data() {
        return {
            width: this.maxWidth || '400px',
        }
    },
    emits: ['close', 'yes', 'no'],
    methods: {
        closeModal() {
            this.$emit('close');
        }
    },
    components: { FontAwesomeIcon }
}
</script>
<style lang="scss">
@use '@/assets/styles/helpers';
@use '@/assets/styles/components';

.modal-enter-active,
.modal-leave-active {
    transition: all 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}


.modal-bg {
    position: fixed;
    inset: 0;
    background-color: rgba($color: #000000, $alpha: 0.5);
    @include helpers.flex-center;
    z-index: 99;

    .modal {
        background-color: var(--color-background-mute);
        max-width: var(--modal-max-width);
        width: 100%;
        padding: 10px;
        border-radius: 20px;
        display: flex;
        flex-direction: column;

        .headline {
            display: flex;
            margin-bottom: 10px;

            .text {
                flex-grow: 1;
                text-align: center;
                font-size: 18px;
            }

            .close-button {
                @include components.button;
                background-color: var(--color-background-mute-4);
                border-radius: 15px;
                padding: 5px;

                svg {
                    width: 15px;
                    height: 15px;
                }
            }
        }

        .modal-content {
            padding: var(--content-padding);
        }

        .modal-buttons {
            display: flex;
            gap: 5px;

            .button {
                @include components.button;
                background-color: var(--color-background-mute-3);
                flex-grow: 1;
                text-align: center;
                padding: 5px;
                border-radius: 10px;
            }
        }
    }
}
</style>