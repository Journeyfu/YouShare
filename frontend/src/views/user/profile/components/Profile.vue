<script setup>

import {ref, watch} from "vue";

const props = defineProps(['profile']) // 名字需要跟ProfileIndex里photo组件给的属性名字保持一致(:photo)
const myProfile = ref(props.profile)

watch(()=> props.profile, newVal => {
    myProfile.value = newVal
})

defineExpose({
   myProfile
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base">Profile</label>
        <textarea v-model="myProfile" rows="6" class="textarea w-108"></textarea>
    </fieldset>

</template>

<style scoped>

</style>