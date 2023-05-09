<template>
    <AppButton active @click="copyText">
        <div class="copy-button">
            <Icon :name="IconsNames.copyIcon" />
            <span>{{ buttonText }}</span>
            <div :class="['copied', { active: coping }]">
                <Icon :name="IconsNames.checkIcon" />
                <span>Скопировано</span>
            </div>
        </div>
    </AppButton>
</template>
<script setup>
import { IconsNames } from "~~/configs/icons";
import { Clipboard } from "v-clipboard";
const { $toast } = useNuxtApp();
const { value } = defineProps({
    value: {
        type: String,
        default: "",
    },
    buttonText: {
        type: String,
        default: "Скопировать",
    },
});
const coping = ref(false);
const copyText = () => {
    coping.value = true;
    try {
        Clipboard.copy(value);
    } catch (error) {
        $toast.error("Не удалось скопировать текст");
    }
    setTimeout(() => {
        coping.value = false;
    }, 1000);
};
</script>
<style lang="scss" scoped>
.copy-button {
    @include flex-center;
    gap: 5px;

    width: 100%;
    height: 100%;
    .copied {
        position: absolute;
        inset: 0;
        opacity: 0;
        background-color: $accent-2;
        @include flex-center;
        gap: 5px;

        &.active {
            opacity: 1;
        }
    }
    .icon {
        width: 20px;
        height: 20px;
    }
}
</style>
