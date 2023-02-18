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
                >
                    <slot name="header"></slot>
                    <div class="modal">
                        <div class="modal-content">
                            <slot name="content"></slot>
                        </div>
                    </div>
                </div>
            </Transition>
        </Teleport>
    </ClientOnly>
</template>
<script setup>
const props = defineProps({
    active: Boolean,
    style: Object,
    yesButton: Boolean,
    yesLoading: Boolean,
    noButton: Boolean,
    offJustifyContent: Boolean,
    maxWidth: {
        type: Number,
        default: 400,
    },
    transition: {
        type: Number,
        default: 250,
    },
    maxWidth: {
        type: Number,
        default: 500,
    },
    maxHeight: {
        type: Number,
        default: 800,
    },

    offOutsideClickClose: {
        type: Boolean,
        default: false,
    },

    gap: {
        type: Number,
        default: 10,
    },
});

const emit = defineEmits(["update:active", "mounted", "close"]);
const transitionString = computed(() => {
    return `${props.transition}ms`;
});
const width = computed(() => {
    return `${props.maxWidth}px`;
});
const height = computed(() => {
    return `${props.maxHeight}px`;
});

const gapString = computed(() => {
    return `${props.gap}px`;
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
        border-radius: 10px;
        display: flex;
        flex-direction: column;

        gap: v-bind(gapString);

        .description {
            font-size: 0.875rem;
            color: $secondary-text;
        }

        .modal-content {
            height: 100%;
        }

        .modal-buttons {
            display: flex;
            gap: 5px;
        }
    }
}
</style>
