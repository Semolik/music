<template>
    <ClientOnly>
        <Teleport to="body" v-if="active || isClosing">
            <Transition name="modal">
                <div
                    :class="[
                        'modal-bg',
                        { open: isActive },
                        { close: isClosing },
                        { 'no-justify-content': props.offJustifyContent },
                    ]"
                    v-if="isActive"
                    @click.self="
                        props.closeButton || props.offOutsideClickClose
                            ? null
                            : closeModal()
                    "
                    v-bind="$attrs"
                    @goToLogin="onGoToLogin"
                >
                    <slot name="header"></slot>
                    <div class="modal">
                        <div class="modal-content">
                            <div class="modal-headline" v-if="props.headText">
                                {{ props.headText }}
                            </div>
                            <slot name="content"></slot>
                        </div>
                        <div
                            class="modal-buttons"
                            v-if="props.buttons.length > 0"
                        >
                            <div
                                :class="[
                                    'button',
                                    {
                                        active: button.active,
                                        disabled: button.active === false,
                                        red: button.red,
                                    },
                                ]"
                                v-for="button in props.buttons"
                                @click="button.onClick"
                            >
                                {{ button.text }}
                            </div>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </ClientOnly>
</template>
<script setup>
import { useEventBus } from "@vueuse/core";
const props = defineProps({
    active: Boolean,
    style: Object,
    offJustifyContent: Boolean,
    transition: {
        type: Number,
        default: 250,
    },
    maxWidth: {
        type: [Number, String],
        default: 500,
    },
    maxHeight: {
        type: [Number, null, String],
        default: 800,
    },
    minHeight: {
        type: [Number, null, String],
        default: null,
    },
    offOutsideClickClose: {
        type: Boolean,
        default: false,
    },
    buttons: {
        type: Array,
        default: () => [],
    },
    gap: {
        type: Number,
        default: 10,
    },
    headText: {
        type: String,
        default: "",
    },
    closeOnEsckey: {
        type: Boolean,
        default: false,
    },
    borderRadius: {
        type: Number,
        default: 10,
    },
});
const modalStateBus = useEventBus("modal-state");
const emit = defineEmits(["update:active", "mounted", "close"]);
const transitionString = computed(() => {
    return `${props.transition}ms`;
});
const width = computed(() => {
    if (typeof props.maxWidth === "string") {
        return props.maxWidth;
    }
    return `${props.maxWidth}px`;
});
const height = computed(() => {
    if (props.maxHeight === null) {
        return "auto";
    }
    if (typeof props.maxHeight === "string") {
        return props.maxHeight;
    }
    return `${props.maxHeight}px`;
});
const borderRadius = computed(() => {
    return `${props.borderRadius}px`;
});
const gapString = computed(() => {
    return `${props.gap}px`;
});
const minHeight = computed(() => {
    if (props.minHeight === null) {
        return "auto";
    }
    if (typeof props.minHeight === "string") {
        return props.minHeight;
    }
    return `${props.minHeight}px`;
});
const isClosing = ref(false);
const isActive = ref(true);
const closeModal = () => {
    isClosing.value = true;
    setTimeout(() => {
        emit("update:active", false);
        emit("close");
        isActive.value = false;
        isClosing.value = false;
    }, props.transition);
};
if (props.closeOnEsckey) {
    onMounted(() => {
        window.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && props.active) {
                closeModal();
            }
        });
    });
}
const openModal = () => {
    isActive.value = true;
    setTimeout(() => {
        emit("mounted");
    }, props.transition);
};
watch(
    () => props.active,
    (value) => {
        if (value) {
            openModal();
        } else {
            closeModal();
        }
    }
);
const unsubscribe = modalStateBus.on((state) => {
    if (state) {
        openModal();
    } else {
        closeModal();
    }
});
onBeforeUnmount(() => {
    unsubscribe();
});
</script>
<style lang="scss">
.modal-enter-active,
.modal-leave-active {
    transition: all v-bind(transitionString) ease;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}

.modal-bg {
    position: fixed;
    inset: 0;
    background-color: rgba($color: #000000, $alpha: 0.5);
    @include flex-center;
    z-index: 99;
    opacity: 0;
    color: $primary-text;
    flex-direction: column;
    transition: opacity v-bind(transitionString) ease-in-out;
    backdrop-filter: blur(8px);
    padding: 10px;
    &.open {
        animation: open v-bind(transitionString) ease-in-out;
        opacity: 1;
    }
    &.close {
        animation: close v-bind(transitionString) ease-in-out;
        opacity: 0;
    }
    &.no-justify-content {
        justify-content: unset;
    }
    @keyframes open {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }
    @keyframes close {
        0% {
            opacity: 1;
        }
        100% {
            opacity: 0;
        }
    }

    .modal {
        background-color: $tertiary-bg;
        max-width: v-bind(width);
        max-height: v-bind(height);
        width: 100%;
        border-radius: v-bind(borderRadius);
        display: flex;
        flex-direction: column;
        padding: 10px;
        gap: v-bind(gapString);
        overflow: auto;
        min-height: v-bind(minHeight);

        .description {
            font-size: 0.875rem;
            color: $secondary-text;
        }

        .modal-content {
            height: 100%;
            display: flex;
            flex-direction: column;
            gap: v-bind(gapString);
            .modal-headline {
                color: $secondary-text;
                font-size: 1.1rem;
                text-align: center;
            }
        }

        .modal-buttons {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;

            .button {
                padding: 5px;
                border-radius: 10px;
                background-color: $quaternary-bg;
                flex-grow: 1;
                text-align: center;
                user-select: none;
                cursor: pointer;
                &:hover {
                    background-color: $quinary-bg;
                }
                &.disabled {
                    background-color: $quaternary-bg;
                    cursor: auto;
                    color: $secondary-text;
                }
                &.active {
                    background-color: $accent;
                    cursor: pointer;
                    color: $primary-bg;
                    &:hover {
                        background-color: $accent-hover;
                    }

                    &.red {
                        background-color: $accent-red;
                        &:hover {
                            background-color: $accent-red-hover;
                        }
                    }
                }
            }
        }
    }
}
</style>
