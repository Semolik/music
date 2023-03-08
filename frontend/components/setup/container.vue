<template>
    <div class="setup-container">
        <div class="info">
            <div class="headline">
                <slot name="headline"></slot>
            </div>
            <div class="description">
                <slot name="description"></slot>
            </div>
        </div>
        <div class="buttons">
            <div class="button">
                <slot name="button"></slot>
            </div>
            <div class="button skip" v-if="skipButton">Пропустить</div>
        </div>
        <div class="content-container">
            <div class="content">
                <slot name="content"></slot>
            </div>
        </div>
    </div>
</template>
<script setup>
const { skipButton } = defineProps({
    skipButton: {
        type: Boolean,
        default: true,
    },
});
</script>
<style scoped lang="scss">
.setup-container {
    display: grid;
    grid-template-columns: min-content 1fr;
    grid-template-rows: 1fr min-content;
    height: 100%;
    --padding: 20px;
    color: $secondary-text;
    width: 100%;
    .buttons {
        grid-column: 1;
        grid-row: 2;
        display: flex;
        flex-direction: column;
        gap: 10px;
        padding-left: var(--padding);
        padding-bottom: var(--padding);
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
        padding-left: var(--padding);

        .headline {
            font-weight: 600;
            text-align: center;
            font-size: 30px;
            white-space: nowrap;
        }
        .description {
            text-align: center;
            font-size: 14px;
        }
    }
    .content-container {
        grid-column: 2;
        grid-row: 1 / 3;
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
            padding-top: 15vh;
            gap: 20px;
        }
    }
}
</style>
