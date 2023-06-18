<template>
    <a class="share-social">
        <a
            :href="`https://t.me/share/url?url=${link}`"
            target="_blank"
            class="share-item tg"
        >
            <Icon :name="IconsNames.telegramIcon" />
        </a>
        <a
            :href="`https://vk.com/share.php?url=${link}`"
            target="_blank"
            class="share-item vk"
        >
            <Icon :name="IconsNames.vkIcon" />
        </a>
    </a>
</template>
<script setup>
import { IconsNames } from "~~/configs/icons";
const { link } = defineProps({
    link: {
        type: String,
        default: "",
    },
});
</script>
<style lang="scss" scoped>
.share-social {
    display: flex;
    gap: 10px;
    .share-item {
        height: 100px;
        flex-grow: 1;
        border-radius: 10px;
        @include flex-center;
        cursor: pointer;
        $tg-color: #0088cc;
        $vk-color: #4a76a8;

        &.tg {
            background-color: $tg-color;

            &:hover {
                background-color: darken($tg-color, 10%);
            }
        }
        &.vk {
            background-color: $vk-color;

            &:hover {
                background-color: darken($vk-color, 10%);
            }
        }
        svg {
            width: 50px;
            height: 50px;
        }
    }
}
</style>
