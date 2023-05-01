<template>
    <card-min v-bind="props" v-if="min" @click="onClick">
        <template #content>
            <span>{{ musician.name }}</span>
        </template>
        <template #card-end>
            <div class="flex justify-center items-center pr-4 secondary-text">
                <Icon name="material-symbols:arrow-forward-ios" />
            </div>
        </template>
    </card-min>
    <div v-else class="musician-card" @click="onClick">
        <card-picture v-bind="props">
            <div class="hover-overlay">
                <div
                    :class="[
                        'favorite',
                        'button',
                        { active: musician.liked },
                        { disabled: !logined },
                    ]"
                    @click.stop="onFavorite"
                >
                    <Icon :name="likeIcon" />
                </div>
                <div class="play button" @click.stop="">
                    <Icon :name="playIcon" />
                </div>
                <div class="more button" @click.stop="ShareModalOpened = true">
                    <Icon :name="shareIcon" />
                </div>
                <ShareModal
                    v-model:active="ShareModalOpened"
                    :link="`/musician/${musician.id}`"
                    add-host
                />
            </div>
        </card-picture>
        <div class="flex flex-col grow text-center primary-text">
            {{ musician.name }}
        </div>
    </div>
</template>
<script setup>
import { Service } from "~~/client";
import { useAuthStore } from "~~/stores/auth";
import { storeToRefs } from "pinia";
import { useEventBus } from "@vueuse/core";
import { IconsNames } from "@/configs/icons";
import { routesNames } from "@typed-router";
const authStore = useAuthStore();
const { logined } = storeToRefs(authStore);
const ShareModalOpened = ref(false);
const { likeIcon, playIcon, shareIcon } = IconsNames;
const goToLoginBus = useEventBus("go-to-login");
const { musician, isLink } = defineProps({
    musician: {
        type: Object,
        required: true,
    },
    min: {
        type: Boolean,
        default: false,
    },
    isLink: {
        type: Boolean,
        default: false,
    },
});
const router = useRouter();
const onClick = () => {
    if (isLink) {
        router.push({
            name: routesNames.musicianId.index,
            params: { id: musician.id },
        });
    }
};
const emit = defineEmits(["update:musician"]);

const props = reactive({
    picture: musician.picture,
    icon: IconsNames.userIcon,
    borderRadius: "50%",
});
const onFavorite = async () => {
    if (!logined.value) {
        goToLoginBus.emit();
        return;
    }
    const { liked, likes_count } =
        await Service.likeMusicianApiV1MusicianProfileIdLikePut(musician.id);
    emit("update:musician", { ...musician, liked });
};
</script>
<style lang="scss" scoped>
.musician-card {
    display: flex;
    flex-direction: column;
    gap: 10px;
    user-select: none;
    color: $secondary-text;
    .hover-overlay {
        cursor: pointer;
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        opacity: 0;
        transition: opacity 0.2s ease-in-out;
        @include flex-center;
        gap: 5px;
        .button {
            border-radius: 50%;
            @include flex-center;
            height: min-content;
            padding: 5px;
            width: 35px;
            height: 35px;
            transition: background-color 0.2s ease-in-out;
            svg {
                height: 100%;
                width: 100%;
            }
            &.play {
                background-color: $accent;
                width: 50px;
                height: 50px;
                &:hover {
                    background-color: $accent-hover;
                }
                svg {
                    color: black;
                }
            }
            &.favorite {
                &:not(.disabled).active {
                    svg {
                        color: $accent-2;
                    }
                }

                &.disabled {
                    background-color: $secondary-bg;

                    &:hover {
                        background-color: $secondary-bg;
                    }
                }
            }
            background-color: $tertiary-bg;
            cursor: pointer;
            &:hover {
                background-color: $quaternary-bg;
            }
        }
    }
    &:hover .hover-overlay {
        opacity: 1;
    }
}
</style>
