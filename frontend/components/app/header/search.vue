<template>
    <ModalDialog
        :active="props.searchActive"
        @update:active="onSearchActiveUpdate"
        id="search-modal"
        :max-width="650"
        :max-height="650"
        off-justify-content
        @close="resetSearchBus.emit()"
        with-event-bus
    >
        <template #header>
            <span class="font-medium mb-2 p-2 text-center">
                Поиск по трекам, альбомам, клипам, исполнителям и плейлистам
            </span>
        </template>
        <template #content>
            <Search ref="searchRef" />
        </template>
    </ModalDialog>
</template>

<script setup>
import { useEventBus } from "@vueuse/core";

const resetSearchBus = useEventBus("reset-search");
const emit = defineEmits(["update:searchActive"]);
const onSearchActiveUpdate = (val) => {
    emit("update:searchActive", val);
};
const searchRef = ref(null);
const props = defineProps({
    searchActive: {
        type: Boolean,
        default: false,
    },
});
</script>

<style lang="scss">
#search-modal {
    padding-top: 20vh;
    .modal {
        border: 1px solid #{$quaternary-text};

        .modal-content {
            width: 100%;
            justify-content: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
            min-height: 250px;
        }
    }
}
</style>
