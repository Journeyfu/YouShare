<script setup>

import {useRoute} from "vue-router";

const route = useRoute()
</script>

<template>
    <!--  get user_id defined in router: "path: '/user/space/:user_id/'"   -->
    My Space: {{ route.params.user_id }}

</template>

<style scoped>

</style>