<template>
    <div class="picture">
        <img :src="picture" alt="profile picture" v-if="picture" />
        <div class="picture-icon">
            <Icon :name="IconsNames.userIcon" />
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
const { picture } = defineProps({
    picture: String | null,
});
</script>
<style lang="scss" scoped>
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
</style>
