<template>
    <div class="content-page-container">
        <div :class="['content-info', { 'is-owner': isOwner }]">
            <div :class="['content-info-bg', { 'no-picture': !picture }]">
                <img class="content-info-bg" :src="picture" v-if="picture" />
            </div>
            <div class="content-picture">
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
                <div class="actions-buttons">
                    <div class="play action-button" @click="$emit('play')">
                        <Icon :name="IconsNames.playIcon" />
                        {{ playButtonText }}
                    </div>
                    <div
                        :class="['like', 'action-button', { active: isLiked }]"
                        @click="$emit('like')"
                    >
                        <Icon :name="IconsNames.likeIcon" />
                        Нравится
                    </div>
                    <div class="action-button" @click="shareModalOpened = true">
                        <Icon :name="IconsNames.shareIcon" />
                        Поделиться
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
const { name, type, picture, info, icon, isOwner, playButtonText, isLiked } =
    defineProps({
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
    .content-info {
        position: relative;
        display: grid;
        gap: 20px;
        isolation: isolate;
        padding: 20px;
        grid-template-columns: 300px 1fr;
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

                    svg {
                        width: 20px;
                        height: 20px;
                        color: $secondary-text;
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
                }
            }
            .info-line {
                display: flex;
                align-items: center;
                gap: 5px;

                &.type {
                    text-transform: uppercase;
                    color: $secondary-text;
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
            }
        }
    }
}
</style>
