<template>
    <FormField placeholder="Поиск" :borderRadius="10"></FormField>
</template>
<script>
import { HTTP } from '../http-common.vue';
import FormField from './FormField.vue';
export default {
    components: {
        FormField
    },
    data() {
        return {
            playlists: []
        }
    },
    mounted(){
        // HTTP.get('')
    }
}
</script>