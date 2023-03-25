<template>
    <div class="request-page">
        <div class="user">
            <RequestsItemContent :request="request" :show-status="showStatus" />
        </div>
        <div class="message">
            {{ request.message }}
        </div>

        <div class="files-list" v-if="request.files.length > 0">
            <a
                v-for="file in request.files"
                :key="file.id"
                class="file"
                :href="file.url"
                :download="file.original_file_name"
            >
                <div class="icon">
                    <Icon name="material-symbols:file-open-rounded" />
                </div>
                {{ file.original_file_name }}
            </a>
        </div>

        <slot />
    </div>
</template>
<script setup>
defineProps({
    request: {
        type: Object,
        required: true,
    },
    showStatus: {
        type: Boolean,
        default: false,
    },
});
</script>
<style lang="scss" scoped>
.request-page {
    display: flex;
    flex-direction: column;
    gap: 10px;
    padding: 10px;
    border-radius: 10px;
    background-color: $quaternary-bg;

    .user {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .message {
        padding: 10px;
        background-color: $quinary-bg;
        border-radius: 5px;
    }
    .files-list {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;

        .file {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-radius: 5px;
            background-color: $secondary-bg;
            transition: all 0.2s ease-in-out;
            .icon {
                width: 20px;
                height: 20px;
                @include flex-center;
                svg {
                    width: 100%;
                    height: 100%;
                }
            }
            &:hover {
                background-color: $accent;
                cursor: pointer;
            }
        }
    }
}
</style>
