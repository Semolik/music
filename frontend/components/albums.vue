<template>
    <ItemsPaginate v-bind="$attrs">
        <template v-slot="{ items }">
            <AlbumCard
                v-for="(album, index) in items"
                :key="album.id"
                v-model:album="items[index]"
            />
        </template>
    </ItemsPaginate>
</template>
