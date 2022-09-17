<template>
    <div class="base-container">
        <slot></slot>
    </div>
</template>

<style>
.base-container {
    width: 100%;
    display: flex;
    gap: 10px;
    flex-direction: column;
}
</style>