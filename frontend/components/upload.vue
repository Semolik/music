<template>
    <el-upload
        class="avatar-uploader"
        :show-file-list="false"
        :before-upload="beforeAvatarUpload"
        v-bind="$attrs"
        :on-success="defaultOnSuccess"
    >
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <Icon :name="IconsNames.userIcon" class="avatar-uploader-icon" v-else />
    </el-upload>
</template>
<script setup>
import { ElMessage } from "element-plus";
import { IconsNames } from "@/configs/icons";
const emit = defineEmits(["success"]);
const defaultOnSuccess = (response, file) => {
    emit("success", file.raw);
};
const { imageUrl, beforeAvatarUpload, handleAvatarSuccess, onSuccess } =
    defineProps({
        imageUrl: {
            type: String,
            default: "",
        },
        borderRadius: {
            type: String,
            default: "50%",
        },
        aspectRatio: {
            type: Number,
            default: 1,
        },
        beforeAvatarUpload: {
            type: Function,
            default: (rawFile) => {
                if (rawFile.type.split("/")[0] !== "image") {
                    ElMessage.error("Это не картинка!");
                    return false;
                } else if (rawFile.size / 1024 / 1024 > 5) {
                    ElMessage.error("Картинка слишком большая!");
                    return false;
                }
                return true;
            },
        },
        onSuccess: {
            type: Function,
        },
    });
</script>

<style lang="scss">
.avatar-uploader {
    width: 100%;
    height: 100%;

    .el-upload {
        position: relative;
        border: 2px dashed transparent;
        border-radius: v-bind(borderRadius);
        cursor: pointer;
        overflow: hidden;
        width: 100%;
        aspect-ratio: v-bind(aspectRatio);
        &::after {
            @include flex-center;
            content: "Изменить";
            flex-direction: column;
            position: absolute;
            inset: 0;
            background-color: rgba(0, 0, 0, 0.5);
            color: #fff;
            opacity: 0;
            transition: opacity 0.3s;
            cursor: pointer;
        }
        &:has(svg) {
            border-color: $quaternary-text;
        }
        &:hover {
            border-color: $accent;
            &::after {
                opacity: 1;
            }
        }
        .avatar-uploader-icon {
            color: #8c939d;
            width: 40px;
            height: 40px;
            text-align: center;
        }
        .avatar {
            width: 100%;
            height: 100%;

            object-fit: cover;
        }
    }
}
</style>
