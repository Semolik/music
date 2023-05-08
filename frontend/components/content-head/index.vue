<template>
    <div class="content-page-container">
        <div :class="['content-info', { 'is-owner': isOwner }]">
            <div :class="['content-info-bg', { 'no-picture': !picture }]">
                <img class="content-info-bg" :src="picture" v-if="picture" />
            </div>
            <div :class="['content-picture', { musician: isMusician }]">
                <img :src="picture" v-if="picture" />
                <div class="icon" v-else>
                    <Icon :name="icon" />
                </div>
            </div>
            <div class="content-info-content">
                <div class="info-line type">
                    {{ type }}
                </div>
                <div class="content-name">
                    {{ name }}
                </div>
                <div class="info-line">
                    <template v-for="(item, index) in info">
                        <ContentHeadInfoItem :item="item" />
                        <div class="dot" v-if="index !== info.length - 1"></div>
                    </template>
                </div>
                <div class="actions-buttons" v-if="!hideAllButtons">
                    <div
                        class="play action-button"
                        @click="$emit('play')"
                        v-if="!hidePlayButton"
                    >
                        <Icon :name="IconsNames.playIcon" />
                        <span class="text">{{ playButtonText }}</span>
                    </div>
                    <div
                        :class="['like', 'action-button', { active: isLiked }]"
                        @click="$emit('like')"
                    >
                        <span class="text">{{ likesCount }}</span>
                        <Icon :name="IconsNames.likeIcon" />
                        <span class="text">Нравится</span>
                    </div>
                    <div class="action-button" @click="shareModalOpened = true">
                        <Icon :name="IconsNames.shareIcon" />
                        <span class="text">Поделиться</span>
                    </div>
                    <div
                        class="action-button edit"
                        @click="$emit('edit')"
                        v-if="isOwner"
                    >
                        <Icon :name="IconsNames.pencilIcon" />
                    </div>
                    <ShareModal
                        v-model:active="shareModalOpened"
                        text="Поделиться"
                        :link="shareLink"
                    />
                </div>
            </div>
            <div class="content-info-actions" v-if="isOwner">
                <div class="content-info-actions-item" @click="$emit('edit')">
                    <Icon :name="IconsNames.pencilIcon" />
                </div>
                <div
                    class="content-info-actions-item"
                    @click="$emit('delete')"
                    v-if="!hideDeleteButton"
                >
                    <Icon :name="IconsNames.deleteIcon" />
                </div>
            </div>
        </div>
        <div class="page-content">
            <slot />
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "~/configs/icons";
const {
    name,
    type,
    picture,
    info,
    icon,
    isOwner,
    playButtonText,
    isLiked,
    hideDeleteButton,
    likesCount,
    isMusician,
    hidePlayButton,
    hideAllButtons,
} = defineProps({
    name: {
        type: String,
        required: true,
    },
    type: {
        type: String,
        required: true,
    },
    picture: {
        type: [String, null],
        required: true,
    },
    info: {
        type: Array,
        required: false,
        default: [],
    },
    icon: {
        type: String,
        required: false,
        default: IconsNames.imageIcon,
    },
    isOwner: {
        type: Boolean,
        required: false,
        default: false,
    },
    isLiked: {
        type: Boolean,
        required: false,
        default: false,
    },
    playButtonText: {
        type: String,
        required: false,
        default: "Воспроизвести",
    },
    hideDeleteButton: {
        type: Boolean,
        required: false,
        default: false,
    },
    likesCount: {
        type: Number,
        required: false,
        default: null,
    },
    isMusician: {
        type: Boolean,
        required: false,
        default: false,
    },
    hidePlayButton: {
        type: Boolean,
        required: false,
        default: false,
    },
    hideAllButtons: {
        type: Boolean,
        required: false,
        default: false,
    },
});
const emit = defineEmits(["edit", "delete", "like", "play"]);
const shareLink = ref("");
onMounted(() => {
    shareLink.value = document.location.href;
});
const shareModalOpened = ref(false);
</script>
<style scoped lang="scss">
.content-page-container {
    display: flex;
    flex-direction: column;
    color: $primary-text;
    height: 100%;
    .page-content {
        height: 100%;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    .content-info {
        position: relative;
        display: grid;
        gap: 20px;
        isolation: isolate;
        padding: 20px;
        grid-template-columns: 300px 1fr;
        @include md(true) {
            @include flex-center;
            flex-direction: column;
        }
        &.is-owner {
            grid-template-columns: 300px 1fr min-content;
            .content-info-actions {
                display: flex;
                flex-direction: column;
                gap: 10px;
                .content-info-actions-item {
                    @include flex-center;
                    width: 45px;
                    height: 45px;
                    @include md(true) {
                        display: none;
                    }

                    border-radius: 10px;
                    background-color: $quinary-bg;
                    cursor: pointer;
                    &:hover {
                        background-color: $senary-bg;
                        svg {
                            color: $primary-text;
                        }
                    }
                    svg {
                        width: 20px;
                        height: 20px;
                        color: $secondary-text;
                    }
                }
            }
        }

        .content-picture {
            width: 100%;
            aspect-ratio: 1;
            border-radius: 10px;
            overflow: hidden;
            @include md(true) {
                max-width: 300px;
            }

            &.musician {
                border-radius: 50%;
            }
            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
            }
            .icon {
                @include flex-center;
                height: 100%;
                width: 100%;
                background-color: $quinary-bg;

                svg {
                    width: 40%;
                    height: 40%;
                    color: $secondary-text;
                }
            }
        }

        .content-info-bg {
            z-index: -1;
            position: absolute;
            inset: 0;
            overflow: hidden;
            &.no-picture {
                background-color: $tertiary-bg;
            }
            img {
                width: 100%;
                height: 100%;
                object-fit: cover;
                filter: blur(20px) brightness(0.7);
            }
        }

        .content-info-content {
            display: flex;
            flex-direction: column;
            justify-content: center;
            overflow: hidden;
            text-overflow: ellipsis;
            gap: 10px;

            .actions-buttons {
                display: flex;
                @include md(true) {
                    @include flex-center;
                }
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 10px;
                .action-button {
                    @include flex-center;
                    padding: 10px 20px;
                    gap: 5px;
                    border-radius: 50px;
                    background-color: $quinary-bg;
                    cursor: pointer;
                    user-select: none;

                    &:hover {
                        background-color: $senary-bg;
                    }
                    @include md(true) {
                        aspect-ratio: 1;
                        .text {
                            display: none;
                        }
                    }
                    svg {
                        width: 20px;
                        height: 20px;
                        color: $secondary-text;
                        @include md(true) {
                            width: 30px;
                            height: 30px;
                        }
                    }

                    &.play {
                        background-color: $accent;
                        color: $primary-bg;

                        svg {
                            color: $primary-bg;
                        }
                        &:hover {
                            background-color: $accent-hover;
                        }
                    }
                    &.like.active svg {
                        color: $accent-error;
                    }
                    &.edit {
                        @include md {
                            display: none;
                        }
                    }
                }
            }
            .info-line {
                display: flex;
                align-items: center;
                gap: 5px;
                @include lg(true) {
                    @include flex-center;
                }
                &.type {
                    text-transform: uppercase;
                    color: $secondary-text;
                    @include md(true) {
                        display: none;
                    }
                }

                .dot {
                    width: 2px;
                    height: 2px;
                    border-radius: 50%;
                    background-color: $secondary-text;
                }
            }
            .content-name {
                --font-size: 4rem;
                line-height: calc(var(--font-size) * 1.1);
                font-size: var(--font-size);
                font-weight: 700;
                text-transform: uppercase;
                overflow: hidden;
                text-overflow: ellipsis;

                @include md(true) {
                    word-wrap: anywhere;
                    text-align: center;
                    --font-size: clamp(2rem, 8vw, 3rem);
                }
            }
        }
    }
}
</style>
