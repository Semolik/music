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
        <div class="image-info-text">
            Изображение имеет соотношение сторон {{ SLIDER_ASPECT_RATIO }}x1,
            рекомендуемый размер {{ width }}x{{ height }}
        </div>
        <div class="info">
            <AppInput
                label="Название слайда"
                :max-length="MAX_SLIDE_NAME_LENGTH"
                :min-length="1"
                v-model="name"
                show-word-limit
                :error="nameError"
            />

            <div class="info-line">
                <el-date-picker
                    v-model="dateRange"
                    type="datetimerange"
                    start-placeholder="Дата открытия"
                    end-placeholder="Дата закрытия"
                    id="date-picker"
                    :style="{
                        '--el-date-editor-width': '100%',
                        '--el-input-height': '100%',
                    }"
                    :clearable="false"
                />

                <div
                    :class="['chekbox', { active: active }]"
                    @click="active = !active"
                >
                    {{ active ? "Активный" : "Неактивный" }}
                </div>
            </div>
            <div class="info-line">
                <AppInput label="Ссылка" :min-length="1" v-model="link" />
                <AppInput
                    label="Cортировка"
                    v-model="order"
                    :formatter="(value) => value.replace(/[^0-9]/g, '')"
                    :max-length="3"
                    :error="orderError"
                />
            </div>
            <div class="buttons">
                <AppButton
                    border-radius="5px"
                    active
                    @click="deleteSlide"
                    class="remove-button"
                    v-if="id"
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
                    {{ id ? "Изменить" : "Создать" }}
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
    },
});
const scaleValue = 400;
const { SLIDER_ASPECT_RATIO, MAX_SLIDE_NAME_LENGTH, DATE_FORMAT } =
    useRuntimeConfig().public;
const slide = reactive(
    id ? await Service.getSlideByIdApiV1SliderSlideIdGet(id) : {}
);
const width = scaleValue * SLIDER_ASPECT_RATIO;
const height = scaleValue;
const title = computed(() =>
    id ? `Редактирование слайда ${slide.name}` : "Создание слайда"
);
const link = ref(id ? slide.url : "");
const name = ref(id ? slide.name : "");
const nameError = computed(() => !name.value);

const picture = ref(id ? slide.picture : "");
const pictureBlob = ref(null);
const order = ref(String(slide?.order || 0));
const orderError = computed(() => !order.value);
const active = ref(id ? slide.is_active : true);

const handleSliderPictureSelect = (file) => {
    picture.value = URL.createObjectURL(file);
    pictureBlob.value = file;
};
const dateStart = computed(() =>
    id ? moment(slide.active_from).toDate() : new Date()
);
const dateEnd = computed(() =>
    id ? moment(slide.active_to).toDate() : new Date()
);
const dateRange = ref([dateStart.value, dateEnd.value]);

const buttonActive = computed(() => {
    return !!(
        !nameError.value &&
        !orderError.value &&
        (id
            ? slide.name !== name.value ||
              slide.is_active !== active.value ||
              slide.url !== link.value ||
              dateEnd.value !== dateRange.value[1] ||
              dateStart.value !== dateRange.value[0] ||
              String(slide.order) !== order.value ||
              pictureBlob.value
            : name.value && pictureBlob.value && dateRange.value[0])
    );
});
const getSendData = () => {
    return {
        slide: JSON.stringify({
            name: name.value,
            is_active: active.value,
            url: link.value,
            active_from: moment(dateRange.value[0]).format(DATE_FORMAT),
            active_to: moment(dateRange.value[1]).format(DATE_FORMAT),
            order: order.value,
        }),
        slide_image: pictureBlob.value,
    };
};
const router = useRouter();
const createSlide = async () => {
    if (!buttonActive.value) return;
    try {
        const response = await Service.createSlideApiV1SliderPost(
            getSendData()
        );
        router.push({
            name: routesNames.adminCabinet.cabinetSliderId,
            params: { id: response.id },
        });
    } catch (error) {
        toast.error(HandleOpenApiError(error).message);
    }
};

const updateSlide = async () => {
    if (!buttonActive.value) return;

    try {
        const response = await Service.updateSlideApiV1SliderSlideIdPut(
            id,
            getSendData()
        );
        for (const key in response) {
            slide[key] = response[key];
        }
        slide.order = String(response.order);
        pictureBlob.value = null;
        dateRange.value = [dateStart.value, dateEnd.value];
    } catch (error) {
        toast.error(HandleOpenApiError(error).message);
    }
};
const deleteSlide = async () => {
    try {
        await Service.deleteSlideApiV1SliderSlideIdDelete(id);
        router.push({ name: routesNames.adminCabinet.cabinetSlider });
    } catch (error) {
        toast.error(HandleOpenApiError(error).message);
    }
};
</script>
<style lang="scss" scoped>
@import url(element-plus/theme-chalk/dark/css-vars.css);
.image-info-text {
    color: $secondary-text;
    font-size: 14px;
}

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
