<template>
    <Transition name="fade">
        <div
            @click="emit('update:filtersMenuOpened', false)"
            class="bg"
            v-if="filtersMenuOpened"
        ></div>
    </Transition>
    <Transition name="fade">
        <div class="filters-menu" ref="filtersMenu" v-if="filtersMenuOpened">
            <div class="headline">{{ headText }}</div>
            <AppSelect
                v-for="(filter, name) in filters"
                :values="filter.values"
                :title="name"
                :model-value="filter.active || filter.default"
                @update:model-value="
                    (event) => !filter.disabled && update(name, event)
                "
                :disabled="filter.disabled"
            />
            <div
                @[filtersIsActived&&`click`]="resetFilters(false)"
                :class="['reset-button', { active: filtersIsActived }]"
            >
                Cбросить фильтры
            </div>
        </div>
    </Transition>
</template>
<script setup>
const { filters, filtersMenuOpened, filtersButton, headText } = defineProps({
    filters: {
        type: Object,
        required: true,
    },
    filtersMenuOpened: {
        type: Boolean,
        required: true,
    },
    filtersButton: {
        type: [null, Object],
        required: true,
    },
    headText: {
        type: String,
        required: false,
        default: "Фильтры",
    },
});

const emit = defineEmits([
    "update:filters",
    "update:filtersMenuOpened",
    "change",
]);
const filtersMenu = ref(null);
onMounted(() => {
    onClickOutside(filtersMenu, (e) => {
        if (e.target === filtersButton) return;
        emit("update:filtersMenuOpened", false);
    });
});
const reseting = ref(false);
const update = (name, value) => {
    if (reseting.value) return;
    filters[name].active = value;
    emit("update:filters", filters);
};

const filtersIsActived = computed(() => {
    return Object.values(filters).some(
        (filter) => filter.active && filter.active !== filter.default
    );
});
watch(filtersIsActived, (value) => {
    emit("change", value);
});
const resetFilters = async () => {
    emit("update:filtersMenuOpened", false);
    reseting.value = true;
    var result = Object.assign({}, filters);
    for (const filter of Object.keys(filters)) {
        result[filter].active = filters[filter].default;
        result[filter].disabled = false;
    }
    emit("update:filters", result);
    reseting.value = false;
};
</script>
<style scoped lang="scss">
.bg {
    position: fixed;
    z-index: 90;
    background-color: rgba(0, 0, 0, 0.5);
    transition: opacity 0.3s ease;
    inset: 0;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.filters-menu {
    position: absolute;
    top: calc(100% + 10px);
    background-color: $quaternary-bg;
    border-radius: 10px;
    padding: 10px;
    z-index: 90;
    display: flex;
    flex-direction: column;
    gap: 10px;
    border: 1px solid $quaternary-text;
    .headline {
        font-size: 20px;
        font-weight: 500;
        color: $primary-text;
        text-align: center;
    }
    @include lg(true) {
        width: 100%;
        position: fixed;
        top: auto;
        bottom: 0;
        left: 0;
        right: 0;
        border: none;
        border-radius: 10px 10px 0 0;
        padding-bottom: 20px;
    }
    .reset-button {
        @include flex-center;
        border-radius: 10px;
        cursor: pointer;
        user-select: none;
        padding: 5px 10px;
        height: min-content;
        background-color: $accent-red;
        color: $primary-bg;

        display: none;
        @include lg(true) {
            display: flex;
            transition: opacity 0.3s ease;
            min-height: 50px;
            &:not(.active) {
                background-color: $quinary-bg;
                color: $secondary-text;
            }
        }
        &.active {
            display: flex;
        }
    }

    .filter-item {
        position: relative;
        &.disabled {
            position: absolute;
            inset: -3px;
            border-radius: 10px;
            background-color: rgba(0, 0, 0, 0.5);
            @include flex-center;

            svg {
                width: 30px;
                height: 30px;
                color: $secondary-text;
            }
        }
    }
}
</style>
