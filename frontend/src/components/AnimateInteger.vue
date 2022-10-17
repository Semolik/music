<!-- https://gist.github.com/millerrafi/65fc1193d98ae9fcef257ab558bc3f2c -->

<template>
    <span class="animate-integer">{{ formatted }}</span>
</template>

<script>
import gsap from 'gsap';
/**
 * A Vue component that displays a value and animates changes.
 *
 * Accepts props for the value; the animation duration; and a method to format the number, e.g. using Intl.NumberFormat.
 */
export default {
    name: 'animate-integer',
    props: {
        value: { default: 0 },
        duration: { default: 0.5 },
        formatter: { type: Function, default: n => n }
    },
    data() {
        return {
            displayValue: Math.ceil(this.value),
            tweenValue: this.value
        };
    },
    computed: {
        formatted() {
            return this.formatter(this.displayValue);
        }
    },
    watch: {
        value() {
            gsap.to(this, {
                tweenValue: Math.ceil(this.value),
                duration: this.duration,
                onUpdate: () => {
                    this.displayValue = Math.round(this.tweenValue);
                },
                onComplete: () => {
                    this.displayValue = Math.round(this.value);
                }
            });
        }
    }
};
</script>