<template>
    <div class="index-selection">
        <div class="selection-head">
            <div class="selection-title">
                <div class="title">
                    {{ title }}
                </div>
                <div class="left-text" v-if="leftText">
                    <nuxt-link :to="leftTextLink" v-if="leftTextLink">
                        {{ leftText }}
                    </nuxt-link>
                    <span v-else>
                        {{ leftText }}
                    </span>
                </div>
            </div>
            <div class="selection-description" v-if="description">
                {{ description }}
            </div>
        </div>
        <div class="selection-content">
            <slot />
        </div>
    </div>
</template>
<script setup>
defineProps({
    title: {
        type: String,
        required: true,
    },
    description: {
        type: String,
        required: false,
    },
    leftText: {
        type: String,
        required: false,
    },
    leftTextLink: {
        type: Object,
        required: false,
        default: null,
    },
});
</script>
<style lang="scss" scoped>
.index-selection {
    display: flex;
    flex-direction: column;
    gap: 20px;

    .selection-head {
        display: flex;
        flex-direction: column;

        .selection-title {
            display: flex;
            flex-direction: row;
            gap: 10px;
            align-items: center;
            .title {
                font-size: 20px;
                font-weight: 600;
                color: $primary-text;
                flex-grow: 1;
            }
            .left-text {
                font-size: 14px;
                font-weight: 400;
                color: $secondary-text;

                &:hover {
                    color: $primary-text;
                }
            }
        }
        .selection-description {
            font-size: 14px;
            font-weight: 400;
            color: $secondary-text;
        }
    }

    .selection-content {
        display: flex;
        flex-direction: column;
        gap: 10px;
        height: min-content;
    }
}
</style>
