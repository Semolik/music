<template>
    <div class="upload-track">
        <div class="line">
            <div class="arrows">
                <div class="arrow" @click="emit('position-up')">
                    <Icon :name="IconsNames.upIcon" />
                </div>
                <div class="arrow" @click="emit('position-down')">
                    <Icon :name="IconsNames.downIcon" />
                </div>
            </div>
            <TrackCard
                :track="track"
                min
                create-track-mode
                @edit="editOpened = !editOpened"
                class="track-card"
            />
        </div>
        <div class="edit" v-if="editOpened">
            <Upload
                border-radius="10px"
                :imageUrl="track.picture"
                class="genre-image-uploader"
                name="trackPicture"
                @file="handleSelectSuccess"
                :icon="IconsNames.imageIcon"
            />
            <div class="fields">
                <AppInput
                    v-model="track.name"
                    label="Название"
                    :max-length="MAX_TRACK_NAME_LENGTH"
                    :min-length="MIN_TRACK_NAME_LENGTH"
                    show-word-limit
                />
                <AppInput
                    v-model="track.feat"
                    label="Создан при участии"
                    :max-length="MAX_TRACK_FEAT_LENGTH"
                    show-word-limit
                />
            </div>
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "~/configs/icons";

const { MAX_TRACK_NAME_LENGTH, MIN_TRACK_NAME_LENGTH, MAX_TRACK_FEAT_LENGTH } =
    useRuntimeConfig().public;
const emit = defineEmits(["position-up", "position-down"]);
const props = defineProps({
    track: {
        type: Object,
        required: true,
    },
});

const blobPicture = ref(null);
const handleSelectSuccess = (file) => {
    track.picture = URL.createObjectURL(file);
    blobPicture.value = file;
};

const track = ref(props.track);
const editOpened = ref(false);
</script>
<style scoped lang="scss">
.upload-track {
    display: flex;
    flex-direction: column;
    gap: 10px;
    .line {
        display: grid;
        grid-template-columns: min-content 1fr;
        gap: 10px;
        width: 100%;

        .track-card {
            width: 100%;
        }

        .arrows {
            display: flex;
            flex-direction: column;
            padding: 3px 0px;
            justify-content: space-between;
            align-items: center;
            user-select: none;

            .arrow {
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background-color: $primary-bg;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
                transition: all 0.3s ease;

                &:hover {
                    background-color: $secondary-bg;
                }
            }
        }
    }
    .edit {
        display: grid;
        grid-template-columns: 200px 1fr;
        gap: 5px;
        padding: 10px;
        border-radius: 10px;
        background-color: $quaternary-bg;

        .fields {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
    }
}
</style>
