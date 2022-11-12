<template>
    <Teleport to="#modal">
        <Transition name="modal">
            <div class="modal-bg" v-if="active" @click.self="closeModal">
                <div class="modal">
                    <div class="headline">
                        <div class="text">{{ headline }}</div>
                        <div class="close-button" @click="closeModal">
                            <FontAwesomeIcon icon="fa-x" />
                        </div>
                    </div>
                    <div class="modal-content">
                        {{ text }}
                    </div>
                    <div class="modal-buttons">
                        <div class="button" v-if="yesButton" @click="$emit('yes')">Да</div>
                        <div class="button" v-if="noButton" @click="$emit('no')">Нет</div>
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>
<script>
import { library } from '@fortawesome/fontawesome-svg-core';
import { faX } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
library.add(faX);

export default {
    props: {
        active: Boolean,
        headline: String,
        text: String,
        yesButton: Boolean,
        noButton: Boolean,
    },
    emits: ['close'],
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
    position: absolute;
    inset: 0;
    background-color: rgba($color: #000000, $alpha: 0.5);
    @include helpers.flex-center;
    z-index: 99;

    .modal {
        background-color: var(--color-background-mute);
        min-width: 400px;
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
            padding: 10px;
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