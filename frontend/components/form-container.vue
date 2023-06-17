<template>
    <div class="form-container">
        <div class="form shadow-2xl">
            <div
                :class="[
                    'message',
                    { active: messageIsShowed },
                    { error: isErrorMessage },
                ]"
            >
                {{ message }}
            </div>
            <div class="headline" v-if="headline">
                {{ headline }}
            </div>
            <div class="description" v-if="description">
                {{ description }}
            </div>
            <slot></slot>
        </div>
        <slot name="bottom"></slot>
    </div>
</template>
<script setup>
const { headline, maxWidth, description } = defineProps({
    headline: String,
    description: String,
    maxWidth: {
        type: String,
        default: "400px",
    },
});
const message = ref("");
const messageIsShowed = ref(false);
const messageTimer = ref(null);
const messageNestedTimer = ref(null);
const isErrorMessage = ref(false);
const showMessage = (messageText, isError) => {
    if (messageTimer.value) {
        clearTimeout(messageTimer.value);
        if (messageNestedTimer.value) {
            clearTimeout(messageNestedTimer.value);
        }
    }
    isErrorMessage.value = isError;
    message.value = messageText;
    messageIsShowed.value = true;
    messageTimer.value = setTimeout(() => {
        messageIsShowed.value = false;
        messageNestedTimer.value = setTimeout(() => {
            message.value = "";
        }, 500);
    }, 3000 * (isError ? 2 : 1));
};
const hideMessage = () => {
    messageIsShowed.value = false;
    message.value = "";
};
defineExpose({
    showMessage,
    hideMessage,
});
</script>
<style scoped lang="scss">
.form-container {
    @include flex-center;
    flex-direction: column;
    gap: 20px;
    height: 100%;

    .form {
        color: $primary-text;
        width: 100%;
        max-width: v-bind(maxWidth);
        padding: 30px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        position: relative;
        background-color: $primary-bg-2;
        border-radius: 10px;
        --app-input-border-radius: 5px;
        @include md(true) {
            padding: 20px;
        }
        .message {
            position: absolute;
            bottom: 110%;
            left: 0;
            width: 100%;
            font-size: 14px;
            text-align: center;
            color: transparent;

            &.active {
                color: $secondary-text;
                &.error {
                    color: $accent-error;
                }
            }
        }
        .description {
            font-size: 14px;

            color: $secondary-text;
            margin-bottom: 10px;
        }
        .headline {
            font-size: 20px;
            font-weight: 500;
            text-align: center;
            color: $secondary-text;
            margin-bottom: 10px;
        }
    }
}
</style>
