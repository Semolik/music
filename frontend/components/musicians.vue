<template>
    <ItemsPaginate v-bind="$attrs">
        <template v-slot="{ items }">
            <MusicianCard
                v-for="(musician, index) in items"
                :key="musician.id"
                v-model:musician="items[index]"
                is-link
            />
        </template>
    </ItemsPaginate>
</template>
