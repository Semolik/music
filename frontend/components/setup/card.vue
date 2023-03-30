<template>
    <div class="card">
        <card-picture v-bind="propsBind" @click="emit('picture-click')">
            <ClientOnly>
                <div
                    :class="[
                        'hover-overlay',
                        { force: forceOverlay || (overlayOnLike && liked) },
                    ]"
                >
                    <div :class="['like-button', { active: liked }]">
                        <Icon :name="IconsNames.likeIcon" />
                    </div>
                </div>
            </ClientOnly>
        </card-picture>
        <div class="card-name">
            <span>{{ name }}</span>
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";

const emit = defineEmits(["picture-click"]);
const { picture, name, liked, icon, forceOverlay, overlayOnLike } = defineProps(
    {
        picture: {
            type: [String, null],
            required: true,
        },
        liked: {
            type: Boolean,
            required: true,
        },
        name: {
            type: String,
            required: true,
        },
        icon: {
            type: String,
            required: false,
        },
        forceOverlay: {
            type: Boolean,
            required: false,
            default: false,
        },
        overlayOnLike: {
            type: Boolean,
            required: false,
            default: true,
        },
    }
);

const propsBind = reactive({
    picture: picture,
    borderRadius: "50%",
    icon: icon,
});
</script>
<style lang="scss" scoped>
.card {
    display: flex;
    flex-direction: column;
    gap: 15px;
    position: relative;

    .hover-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: rgba(0, 0, 0, 0.5);
        opacity: 0;
        transition: opacity 0.2s ease-in-out;

        &.force,
        &:hover {
            opacity: 1;
        }

        .like-button {
            display: flex;
            justify-content: center;
            align-items: center;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: $tertiary-text;
            cursor: pointer;
            transition: 0.2s;

            &.active {
                background-color: $quaternary-bg;
                svg {
                    color: red;
                }
            }
            svg {
                color: black;
                width: 100%;
                height: 100%;
            }
        }
    }

    .card-name {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
        span {
            font-weight: 500;
        }
    }
}
</style>
