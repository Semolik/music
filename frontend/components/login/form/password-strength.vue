<template>
    <div class="password-strength">
        <div class="bar">
            <ClientOnly>
                <div
                    :class="['progress', `id-${strength.id}`]"
                    :style="{
                        width: `${
                            strength.length > 0 ? (strength.id + 1) * 25 : 0
                        }%`,
                    }"
                />
            </ClientOnly>
        </div>

        <div class="password-contain">
            <div
                :class="[
                    'password-contain-item',
                    {
                        active: containLowerAndUpper,
                    },
                ]"
            >
                <Icon name="material-symbols:check-circle" />
                <div class="password-contain-item__text">
                    <span>Содержит верхний и нижний регистр</span>
                </div>
            </div>
            <div
                :class="[
                    'password-contain-item',
                    {
                        active: containNumber,
                    },
                ]"
            >
                <Icon name="material-symbols:check-circle" />
                <div class="password-contain-item__text">
                    <span>Содержит цифры</span>
                </div>
            </div>
            <div
                :class="[
                    'password-contain-item',
                    {
                        active: containsSymbols,
                    },
                ]"
            >
                <Icon name="material-symbols:check-circle" />
                <div class="password-contain-item__text">
                    <span>Содержит специальные символы</span>
                </div>
            </div>

            <div
                :class="[
                    'password-contain-item',
                    {
                        active: containsMoreThan10,
                    },
                ]"
            >
                <Icon name="material-symbols:check-circle" />
                <div class="password-contain-item__text">
                    <span>Содержит 10 и более символов</span>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import { passwordStrength } from "check-password-strength";

const props = defineProps({
    password: {
        type: String,
        required: true,
    },
});
const runtimeConfig = useRuntimeConfig();
const { MIN_PASSWORD_LENGTH } = runtimeConfig.public;
const strength = computed(() => {
    return passwordStrength(props.password, [
        {
            id: 0,
            value: "Too weak",
            minDiversity: 0,
            minLength: 0,
        },
        {
            id: 1,
            value: "Weak",
            minDiversity: 2,
            minLength: MIN_PASSWORD_LENGTH,
        },
        {
            id: 2,
            value: "Medium",
            minDiversity: 4,
            minLength: MIN_PASSWORD_LENGTH,
        },
        {
            id: 3,
            value: "Strong",
            minDiversity: 4,
            minLength: 10,
        },
    ]);
});
const containLowerAndUpper = computed(() => {
    return ["lowercase", "uppercase"].every((rule) =>
        strength.value.contains.includes(rule)
    );
});
const containNumber = computed(() => {
    return strength.value.contains.includes("number");
});
const containsSymbols = computed(() => {
    return strength.value.contains.includes("symbol");
});

const containsMoreThan10 = computed(() => {
    return strength.value.length >= 10;
});
</script>
<style lang="scss" scoped>
.password-strength {
    display: flex;
    flex-direction: column;
    gap: 10px;

    .bar {
        width: 100%;
        height: 5px;
        background-color: $tertiary-bg;
        border-radius: 5px;
        overflow: hidden;
        .progress {
            height: 100%;
            background-color: $accent-success;
            transition: width 0.3s ease;
            &.id-0 {
                background-color: $accent-error;
            }
            &.id-1 {
                background-color: $accent-warning;
            }
            &.id-2 {
                background-color: $accent-success;
            }
        }
    }

    .password-contain {
        display: flex;
        flex-direction: column;
        gap: 5px;

        .password-contain-item {
            display: flex;
            align-items: center;
            gap: 10px;
            &.active {
                svg {
                    color: $accent-success;
                }
                span {
                    color: $accent-success;
                }
            }
            svg {
                width: 15px;
                height: 15px;
                color: $secondary-text;
            }
            &__text {
                span {
                    font-size: 15px;
                    color: $secondary-text;
                }
            }
        }
    }
}
</style>
