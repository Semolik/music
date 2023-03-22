<template>
    <NuxtLink to="/settings/profile" class="logined-info">
        <UserAvatar :picture="picture" />
        <span>{{ fullName }}</span>
    </NuxtLink>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
const { fullName, picture } = defineProps({
    fullName: String,
    picture: String | null,
});
const { userIcon } = IconsNames;
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
}
</style>
