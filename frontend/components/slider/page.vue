<template>
    <SettingsPage :title="title" max-width="100%" padding="10px">
        <Upload
            @file="handleSliderPictureSelect"
            name="slide_image"
            border-radius="5px"
            :icon="IconsNames.imageIcon"
            :aspect-ratio="SLIDER_ASPECT_RATIO"
            :imageUrl="picture"
        />
        <div class="info">
            <div class="info-line">
                <AppInput
                    label="Название слайда"
                    :max-length="MAX_SLIDE_NAME_LENGTH"
                    :min-length="1"
                    v-model="name"
                    show-word-limit
                    :error="nameError"
                />
                <AppInput
                    label="Cортировка"
                    v-model="order"
                    :formatter="(value) => value.replace(/[^0-9]/g, '')"
                    :max-length="3"
                />
            </div>
            <div class="info-line">
                <DateRangePicker v-model="dateRange" />
                <div
                    :class="['chekbox', { active: active }]"
                    @click="active = !active"
                >
                    {{ active ? "Активный" : "Неактивный" }}
                </div>
            </div>
            <AppInput
                label="Ссылка"
                :min-length="1"
                v-model="link"
                :error="linkError"
            />
            <div class="buttons">
                <AppButton
                    border-radius="5px"
                    active
                    v-if="id"
                    class="remove-button"
                >
                    Удалить
                </AppButton>
                <AppButton
                    :active="buttonActive"
                    border-radius="5px"
                    @click="
                        (event) =>
                            id ? updateSlide(event) : createSlide(event)
                    "
                >
                    {{ id ? "Сохранить" : "Создать" }}
                </AppButton>
            </div>
        </div>
    </SettingsPage>
</template>
<script setup>
import { Service } from "~~/client";
import { IconsNames } from "~~/configs/icons";
import { routesNames } from "@typed-router";
import moment from "moment";
import { useToast } from "vue-toastification";
const toast = useToast();
const { id } = defineProps({
    id: {
        type: String,
        required: true,
    },
});
const { SLIDER_ASPECT_RATIO, MAX_SLIDE_NAME_LENGTH } =
    useRuntimeConfig().public;
const slide = ref(
    id ? await Service.getSlideByIdApiV1SliderSlideIdGet(id) : {}
);
const title = computed(() =>
    id ? `Редактирование слайда ${slide.value.name}` : "Создание слайда"
);
const link = ref(id ? slide.value.url : "");
const name = ref(id ? slide.value.name : "");
const nameError = computed(() => !name.value);
const linkError = computed(() => !link.value);
const picture = ref(id ? slide.value.picture : "");
const pictureBlob = ref(null);
const order = ref(id ? slide.value.order : null);
const active = ref(id ? slide.value.is_active : true);
const buttonActive = computed(() => !nameError.value && !linkError.value);
const handleSliderPictureSelect = (file) => {
    picture.value = URL.createObjectURL(file);
    pictureBlob.value = file;
};
const dateRage = ref(
    id
        ? [
              moment(slide.value.startDate).format("DD.MM.YYYY h:mm"),
              moment(slide.value.endDate).format("DD.MM.YYYY h:mm"),
          ]
        : [new Date(), null]
);

const router = useRouter();
const createSlide = async (event) => {
    if (!buttonActive.value) return;

    try {
        const response = await Service.createSlideApiV1SliderPost({
            name: name.value,
            is_active: active.value,
            url: link.value,
            active_from: dateRage.value[0].toString(),
            active_to: dateRage.value[1].toString(),
            slide_image: pictureBlob.value,
            order: order.value,
        });
        router.push({
            to: routesNames.adminCabinet.cabinetSliderId,
            params: { id: response.id },
        });
    } catch (error) {
        toast.error(HandleOpenApiError(error).message);
    }
};

const updateSlide = async (event) => {
    if (!buttonActive.value) return;

    try {
        const response = await Service.updateSlideApiV1SliderSlideIdPut(id, {
            name: name.value,
            is_active: active.value,
            url: link.value,
            active_from: dateRage.value[0].toString(),
            active_to: dateRage.value[1].toString(),
            slide_image: pictureBlob.value,
            order: order.value,
        });
        slide.value = response;
    } catch (error) {
        toast.error(HandleOpenApiError(error).message);
    }
};
</script>
<style lang="scss" scoped>
.info {
    display: flex;
    flex-direction: column;
    gap: 10px;
    height: 100%;
    --app-input-border-radius: 5px;
    .info-line {
        display: grid;
        gap: 10px;
        grid-template-columns: 1fr 120px;
        .chekbox {
            @include flex-center;
            border-radius: 5px;
            cursor: pointer;
            padding: 10px;
            background-color: $secondary-bg;
            color: $secondary-text;
            user-select: none;
            transition: all 0.1s ease-in-out;
            &.active {
                background-color: $accent;
                color: $primary-bg;
            }
        }
    }
    .buttons {
        display: flex;
        gap: 10px;
        .remove-button {
            --app-button-active-hover-bg: #{$accent-error};
            --app-button-active-bg: #{$accent-red};
        }
    }
}
</style>