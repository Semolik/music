<template>
    <div class="requests-container">
        <status-history-item :request="request" v-for="request in this.requests" />
    </div>
</template>
<style lang="scss">
.requests-container {
    display: flex;
    flex-direction: column;
    gap: 5px;
}
</style>
<script>
import { HTTP } from '../http-common.vue';
import StatusHistoryItem from './PersonalAccountChangeStatusHistoryItem.vue';

export default {
    data() {
        return {
            requests: []
        };
    },
    mounted() {
        HTTP.get("change-role")
            .then((response) => {
                this.requests = response.data;
            })
            .catch((error) => {
                this.requests = [];
            });
    },
    components: { StatusHistoryItem }
}
</script>