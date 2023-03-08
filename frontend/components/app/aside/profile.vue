<template>
    <NuxtLink to="/settings/profile" class="logined-info">
        <div class="picture">
            <img :src="picture" alt="profile picture" v-if="picture" />
            <div class="picture-icon">
                <Icon :name="musicianIcon" />
            </div>
        </div>
        <span>{{ fullName }}</span>
    </NuxtLink>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
const { fullName, picture } = defineProps({
    fullName: String,
    picture: String | null,
});
const { musicianIcon } = IconsNames;
</script>
<style lang="scss" scoped>
.logined-info {
    display: flex;
    gap: 10px;
    align-items: center;
    text-decoration: none;
    color: $secondary-text;
    background-color: $tertiary-bg;
    padding: 5px;
    border-radius: 5px;
    cursor: pointer;
    &:hover {
        background-color: $quaternary-bg;
    }
    .picture {
        width: 50px;
        height: 50px;
        border-radius: 5px;
        overflow: hidden;
        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .picture-icon {
            @include flex-center;
            width: 100%;
            height: 100%;
            background-color: $secondary-bg;
            svg {
                width: 30px;
                height: 30px;
                fill: $secondary-text;
            }
        }
    }
}
</style>
