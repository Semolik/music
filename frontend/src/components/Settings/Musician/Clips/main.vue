<template>
    <FormField placeholder="Поиск" :borderRadius="7" v-model="text" off-margin>
        <template v-slot:side>
            <router-link to="/lk/my-music/clips/add" class="add-clip-button">
                <FontAwesomeIcon icon='fa-plus' />
            </router-link>
        </template>
    </FormField>
</template>
<script>
import { HTTP } from '/src/http-common.vue';
import FormField from '/src/components/FormField.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPlus } from '@fortawesome/free-solid-svg-icons';
library.add(faPlus)
export default {
    components: { FormField, FontAwesomeIcon },
    async setup() {
        const { data: clips } = await HTTP.get("clips/my");
        return { clips }
    },
    data() {
        return {
            text: ''
        }
    }
}
</script>
<style lang="scss">
@use '@/assets/styles/components';

.add-clip-button {
    @include components.button;
    @include components.button-sizes;
    outline: 1px solid var(--fields-border-color);
    background-color: var(--color-background-mute-4);

    &:hover {
        background-color: var(--color-background-mute-5);
    }
}
</style>