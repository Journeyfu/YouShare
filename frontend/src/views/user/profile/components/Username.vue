<script setup>

import {ref, watch} from "vue";

const props = defineProps(['username']) // 名字需要跟ProfileIndex里photo组件给的属性名字保持一致(:username) 这里只是定义
const myUsername = ref(props.username)

// 为了在拉取云端信息后第一时间获取数据，需要把props同步到myUsername上
watch(()=> props.username, newVal => {
    myUsername.value = newVal
})

defineExpose({
   myUsername
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base">Username</label>
        <input v-model="myUsername" type="text" class="input w-108">
    </fieldset>
</template>

<style scoped>

</style>