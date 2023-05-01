<template>
    <ItemsPaginate v-bind="$attrs" :mdWidth="250" :width="300">
        <template v-slot="{ items }">
            <ClipCard
                v-for="(clip, index) in items"
                :key="clip.id"
                v-model:clip="items[index]"
            />
        </template>
    </ItemsPaginate>
</template>
