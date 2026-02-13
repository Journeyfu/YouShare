<script setup>
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icon/CameraIcon.vue";
import Croppie from "croppie"
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

watch(()=> props.photo, newVal => {
    myPhoto.val = newVal
})

const fileInputRef = useTemplateRef("file-input-ref")
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

async function openModal(photo){
    modalRef.value.showModal()
    await nextTick()
    if (!croppie) {
    croppie = new Croppie(croppieRef.value, {  // 创建croppie对象
        viewport: {width: 200, height: 200, type: 'square'},
        boundary: {width: 300, height: 300},
        enableOrientation: true,
        enforceBoundary: true,
      })
    }

    croppie.bind({
        url: photo
    })
}

async function crop(){
    if(!croppie) return

    myPhoto.value = await croppie.result({
        type: 'base64',
        size: 'viewpoint',
    })
    modalRef.value.close()
}

function onFileChange(e){
    const file = e.target.files[0]
    e.target.value = '' // 确保可以上传同一张图片
    if(!file) return

    const reader = new FileReader()

    reader.onload = ()=>{
        openModal(reader.result)
    }
    reader.readAsDataURL(file)
}

onBeforeUnmount(()=>{
    croppie?.destroy()
})

defineExpose({
    myPhoto
})

</script>

<template>
    <div class="flex justify-center">
        <div class="avatar relative">
            <div v-if="myPhoto" class="w-28 rounded-full">
                <img :src="myPhoto" alt="">
            </div>
            <div v-else class="w-28 h-28 rounded-full bg-base-200"></div>
            <div @click="fileInputRef.click()"  class="w-28 h-28 rounded-full bg-black/20 absolute left-0 top-0 flex justify-center items-center cursor-pointer">
                <CameraIcon />
            </div>
        </div>
    </div>

    <input ref=file-input-ref type="file" class="hidden" accept="image/*" @change="onFileChange">

    <dialog ref="modal-ref" class="modal">
        <div class="modal-box transition-none">
            <button @click="modalRef.close()" class="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>

            <div ref="croppie-ref" class="flex flex-col my-4"></div>

            <div class="modal-action">
                <button @click="modalRef.close()" class="btn">Close</button>
                <button @click="crop" class="btn btn-neutral">Confirm</button>
            </div>
        </div>
    </dialog>

</template>

<style scoped>

</style>