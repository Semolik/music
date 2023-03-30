<template>
    <div class="setup-container">
        <div class="info" id="setup-info">
            <div class="headline">
                <slot name="headline"></slot>
            </div>
            <div class="description">
                <slot name="description"></slot>
            </div>
        </div>
        <div class="buttons">
            <slot name="buttons"></slot>
            <div class="button" @click="emit('next')" v-if="nextButton">
                Далее
            </div>
            <div class="button skip" v-if="skipButton" @click="emit('skip')">
                Пропустить
            </div>
        </div>
        <div class="content-container">
            <div class="content">
                <Teleport
                    to="#setup-info"
                    :disabled="$viewport.isGreaterOrEquals('lg')"
                    v-if="mounted"
                >
                    <div class="search-container">
                        <AppInput
                            :model-value="search"
                            @update:model-value="onUpdateSearch"
                            :placeholder="placeholder"
                            class="setup-input"
                            size="large"
                            height="50px"
                            v-if="search !== null"
                        />
                    </div>
                </Teleport>
                <slot name="content"></slot>
                <ClientOnly>
                    <div class="items" v-auto-animate>
                        <slot name="items"></slot>
                    </div>
                </ClientOnly>
            </div>
        </div>
        <ModalDialog
            :active="modalActive"
            @update:model-value="(value) => emit('update:modalActive', value)"
            @close="emit('update:modalActive', false)"
            :buttons="modalButtons"
        >
            <template #content>
                <div class="warning-modal">
                    <div class="warning-modal-headline">
                        {{ modalHeadline }}
                    </div>
                    <div class="warning-modal-description">
                        {{ modalDescription }}
                    </div>
                </div>
            </template>
        </ModalDialog>
    </div>
</template>
<script setup>
const {
    skipButton,
    nextButton,
    search,
    placeholder,
    modalActive,
    modalButtons,
    modalDescription,
    modalHeadline,
} = defineProps({
    skipButton: {
        type: Boolean,
        default: true,
    },
    nextButton: {
        type: Boolean,
        default: true,
    },
    search: {
        type: String,
        default: null,
    },
    placeholder: {
        type: String,
        default: "Поиск",
    },
    modalActive: {
        type: Boolean,
        default: false,
    },
    modalButtons: {
        type: Array,
        default: () => [],
    },
    modalDescription: {
        type: String,
        default: "",
    },
    modalHeadline: {
        type: String,
        default: "",
    },
});

const emit = defineEmits([
    "skip",
    "next",
    "update:search",
    "update:modalActive",
]);
const onUpdateSearch = (value) => emit("update:search", value);
const mounted = ref(false);
onMounted(() => {
    mounted.value = true;
});
</script>
<style scoped lang="scss">
.warning-modal {
    display: flex;
    gap: 10px;
    flex-direction: column;
    .warning-modal-headline {
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
    }
    .warning-modal-description {
        font-size: 1rem;
        font-weight: 400;
    }
}
.setup-container {
    display: grid;
    grid-template-columns: min-content 1fr;

    height: 100%;
    --padding: 20px;
    color: $secondary-text;
    width: 100%;
    @include lg(true) {
        grid-template-columns: 1fr;
        grid-template-rows: min-content 1fr;
    }
    @include lg {
        grid-template-rows: 1fr min-content;
    }
    .search-container {
        display: flex;
        width: 100%;
    }
    .buttons {
        grid-column: 1;
        grid-row: 2;
        display: flex;
        flex-direction: column;
        gap: 10px;
        @include lg {
            padding-left: var(--padding);
            padding-bottom: var(--padding);
        }
        @include lg(true) {
            padding: 10px;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            z-index: 100;
            background-color: rgba($primary-bg, $alpha: 0.5);
            backdrop-filter: blur(20px);
        }
        .button {
            @include flex-center;
            background-color: $accent;
            color: black;
            padding: 10px;
            border-radius: 10px;
            cursor: pointer;
            transition: 0.2s;
            &:hover {
                background-color: $accent-hover;
            }

            &.skip {
                background-color: $quaternary-bg;
                color: $accent;
                &:hover {
                    background-color: $tertiary-bg;
                }
            }
        }
    }

    .info {
        @include flex-center;
        flex-direction: column;
        gap: 30px;
        @include lg(true) {
            gap: 10px;
            padding-top: 20px;
            padding-inline: 10px;
        }
        @include lg {
            padding-left: var(--padding);
        }
        .headline {
            font-weight: 600;
            text-align: center;
            font-size: 30px;
            @include lg {
                white-space: nowrap;
            }
            @include lg(true) {
                font-size: 20px;
            }
        }
        .description {
            text-align: center;
            font-size: 14px;
            @include lg(true) {
                margin-bottom: 10px;
            }
        }
    }
    .content-container {
        @include lg {
            grid-column: 2;
            grid-row: 1 / 3;
        }
        @include flex-center;
        height: 100%;
        overflow-y: scroll;
        .content {
            display: flex;
            flex-direction: column;
            width: 100%;
            height: 100%;
            max-width: 1000px;
            padding: 20px;
            gap: 20px;

            @include lg {
                padding-top: 15vh;
            }
            .setup-input {
                font-size: 1rem;
                margin-bottom: 20px;
            }
            .items {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                grid-auto-rows: min-content;
                gap: 20px;
                width: 100%;
            }
        }
    }
}
</style>
