<template>
    <form class="add-clip-container">
        <SelectImage not-empty :disabled="saveImageFromUrl" @changed="image = $event" />
        <div class="clip-content">
            <FormField :force-wrong="!youtubeId" v-model="url" :border-radius="10"
                label="Ссылка на видеоролик с youtube" />
            <Checkbox v-model="saveImageFromUrl" label="Использовать превью ролика как изображние" />
            <SaveBlock :wrong="wrong" :active="!wrong"/>
        </div>
    </form>
</template>
<script>
import { HTTP } from '/src/http-common.vue';
import Checkbox from '/src/components/checkbox.vue';
import FormField from '/src/components/FormField.vue';
import SelectImage from '/src/components/SelectImage.vue';
import SaveBlock from '/src/components/Settings/SaveBlock.vue';
export default {
    components: { FormField, SelectImage, SaveBlock, Checkbox },
    data() {
        return {
            url: '',
            saveImageFromUrl: false,
            image: null
        }
    },
    methods: {
        create(){
            HTTP.post('')
        }
    },
    computed: {
        youtubeId() {
            var result = /http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?/.exec(this.url)
            return result ? result[1] : null
        },
        wrong() {
            return !this.youtubeId || !(this.saveImageFromUrl ? true : this.image);
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/components';

.add-clip-container {
    @include components.container-with-select-image;

    .clip-content {
        display: flex;
        flex-direction: column;
    }
}
</style>