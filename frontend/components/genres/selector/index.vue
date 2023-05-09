<template>
    <div class="genres-selector" v-bind="$attrs">
        <div
            @click="
                maxSelected
                    ? showMaxGenresMessage()
                    : (searchGenresModelActive = true)
            "
            :class="['genre add', { disabled: maxSelected }]"
        >
            <Icon :name="IconsNames.plusIcon" />
            <span>Добавить жанр</span>
        </div>

        <div
            class="genre"
            v-for="genre in modelValue"
            :key="genre.id"
            @click="onRemoveGenre(genre)"
        >
            <span>{{ genre.name }}</span>
        </div>
    </div>

    <ModalDialog
        :active="searchGenresModelActive"
        @close="searchGenresModelActive = false"
        head-text="Поиск жанра"
        closeOnEsckey
        :min-height="400"
        max-height="60vh"
    >
        <template #content>
            <AppInput
                v-model="search"
                placeholder="Поиск жанра"
                :style="{ '--app-input-border-radius': '5px' }"
            />
            <ClientOnly>
                <div class="search-genres" v-auto-animate>
                    <GenresSelectorSearchItem
                        v-for="genre in searchGenres"
                        :key="genre.id"
                        :genre="genre"
                        :active="selectedGenresIds.includes(genre.id)"
                        @add="onAddGenre"
                        @remove="onRemoveGenre"
                    />
                </div>
            </ClientOnly>
            <NotFound v-if="searchGenres.length === 0" />
        </template>
    </ModalDialog>
</template>
<script setup>
import { IconsNames } from "~/configs/icons";
import { Service } from "~/client";
const startGenres = await Service.getGenresApiV1GenresGet(1);
const { MAX_SELECT_GENRES_COUNT } = useRuntimeConfig().public;
const search = ref("");
const props = defineProps({
    modelValue: {
        type: Array,
        required: true,
    },
});
const modelValue = computed({
    get: () => props.modelValue,
    set: (value) => emit("update:modelValue", value),
});
const { $toast } = useNuxtApp();
const selectedGenresIds = computed(() => modelValue.value.map((g) => g.id));
const maxSelected = computed(
    () => modelValue.value.length >= MAX_SELECT_GENRES_COUNT
);
const showMaxGenresMessage = () => {
    $toast.error(
        `Вы не можете выбрать больше ${MAX_SELECT_GENRES_COUNT} жанров`
    );
};
const onAddGenre = (genre) => {
    if (maxSelected.value) {
        showMaxGenresMessage();
        return;
    }
    modelValue.value = [...modelValue.value, genre];
};
const onRemoveGenre = (genre) => {
    modelValue.value = modelValue.value.filter((g) => g.id !== genre.id);
};
const searchGenresModelActive = ref(false);
const searchGenres = ref([]);
const emit = defineEmits(["update:modelValue"]);
watch(
    search,
    async (value) => {
        if (!value) {
            searchGenres.value = startGenres;
            return;
        }
        searchGenres.value = await Service.getGenresApiV1SearchGenresGet(value);
    },
    { immediate: true }
);
</script>
<style scoped lang="scss">
.search-genres {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 10px;
}
.genres-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;

    .genre {
        @include flex-center;
        gap: 5px;
        padding: 8px 30px;
        border-radius: 10px;
        background-color: $quinary-bg;
        cursor: pointer;
        height: min-content;
        user-select: none;
        &.add {
            flex-grow: 0;

            &.disabled {
                opacity: 0.5;
                cursor: auto;
            }
        }
        flex-grow: 1;
        span {
            font-weight: 500;
            color: $primary-text;
        }
        svg {
            width: 18px;
            height: 18px;
        }

        &:not(.disabled):hover {
            background-color: $senary-bg;
        }
    }
}
</style>
