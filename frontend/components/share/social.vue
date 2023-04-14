<template>
    <div class="share-social">
        <div class="share-item tg">
            <a :href="`https://t.me/share/url?url=${link}`" target="_blank">
                <Icon :name="IconsNames.telegramIcon" />
            </a>
        </div>
        <div class="share-item vk">
            <a :href="`https://vk.com/share.php?url=${link}`" target="_blank">
                <Icon :name="IconsNames.vkIcon" />
            </a>
        </div>
    </div>
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
        &.tg {
            background-color: #0088cc;
        }
        &.vk {
            background-color: #0077ff;
        }
        svg {
            width: 50px;
            height: 50px;
        }
    }
}
</style>
