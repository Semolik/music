<template>
    <div class="requests-container">
        <div class="request" v-for="request in requests"> {{request}}</div>
    </div>
</template>

<script>
import { HTTP } from '../http-common.vue';

export default {
    data() {
        return {
            requests: []
        }
    },
    mounted() {
        HTTP.get('change-role')
            .then((response) => {
                this.requests = response.data;
            })
            .catch((error) => {
                this.requests = [];
            });
    }
}
</script>