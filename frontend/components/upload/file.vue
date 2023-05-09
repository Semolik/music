<template>
    <div class="upload-file">
        <input type="file" @change="handleSelect" :accept="fileTypes" />
        <div class="preview" v-if="file">
            <div class="name">
                <span>{{ file.name }}</span>
            </div>
            <span>{{ fileSizeMB }} MB</span>
        </div>
        <div class="preview empty" v-else>
            <div class="info">
                <Icon :name="IconsNames.fileIcon" />
                <span>Выберите файл</span>
            </div>
            <span class="description">
                Размер файла не должен превышать {{ fileSize }} MB
            </span>
        </div>
    </div>
</template>
<script setup>
import { IconsNames } from "@/configs/icons";
const { $toast } = useNuxtApp();
const { fileSize, fileTypes, url } = defineProps({
    fileSize: {
        type: Number,
        default: null,
    },
    fileTypes: {
        type: Array,
        default: () => [],
    },
});
const emit = defineEmits(["file"]);
const file = ref(null);

const handleSelect = (e) => {
    const event_file = e.target.files[0];
    if (!event_file) {
        file.value = null;
        emit("file", file.value);
        return;
    }
    if (fileTypes.length && !fileTypes.includes(event_file.type)) {
        $toast.error("Неверный тип файла");
        return;
    }
    if (fileSize && event_file.size > fileSize * 1024 * 1024) {
        $toast.error(`Размер файла превышает ${fileSize} MB`);
        return;
    }
    file.value = event_file;
    emit("file", file.value);
};
const fileSizeMB = computed(() => {
    if (!file.value) return;
    return (file.value.size / 1024 / 1024).toFixed(2);
});
</script>
<style scoped lang="scss">
.upload-file {
    @include flex-center;
    position: relative;
    width: 100%;
    min-height: 100px;
    border: 2px dashed $quaternary-text;
    border-radius: 10px;
    padding: 20px;

    &:hover {
        border-color: $accent;
    }
    input {
        position: absolute;
        inset: 0;
        opacity: 0;
        cursor: pointer;
    }
    .preview {
        width: 100%;
        @include flex-center;
        gap: 5px;
        text-align: center;
        &.empty {
            flex-direction: column;
        }

        .info {
            @include flex-center;
            gap: 5px;
        }
        .description {
            color: $secondary-text;
            font-size: 12px;
        }
    }
}
</style>
