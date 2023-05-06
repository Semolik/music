<template>
    <ItemsPaginate v-bind="$attrs" is-tracks>
        <template v-slot="{ items }">
            <TrackCard
                v-for="(track, index) in items"
                :key="track.id"
                v-model:track="items[index]"
            />
        </template>
    </ItemsPaginate>
</template>
