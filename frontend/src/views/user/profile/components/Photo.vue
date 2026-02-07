<script setup>
import {nextTick, onBeforeMount, onBeforeUnmount, ref, useTemplateRef, vModelRadio, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icon/CameraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo']) // 名字需要跟ProfileIndex里photo组件给的属性名字保持一致(:photo)
const myPhoto = ref(props.photo)


watch(()=> props.photo, newVal => {
    myPhoto.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie = null

async function openModal(photo) {
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
        url: photo,
    })
}
async function crop(){
    if(!croppie) return
    myPhoto.value = await croppie.result({
        type: "base64",
        size: "viewpoint",
    })
    modalRef.value.close()
}

function onFileChange(e){
    const file = e.target.files[0]
    e.target.value = ''
    if(!file) return
    const reader = new FileReader()
    reader.onload = () =>{
        openModal(reader.result)
    }

    reader.readAsDataURL(file)
}

onBeforeUnmount(()=> {
    croppie?.destroy()
})

defineExpose({
    myPhoto
})
</script>

<template>
    <div class="flex justify-center">
        <div class="avatar relative">
            <div class="w-28 rounded-full">
                <img :src="myPhoto" alt="">
            </div>
            <div @click="fileInputRef.click()" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
                <!--  头像上渲染个相机   -->
                <CameraIcon />
            </div>
        </div>
    </div>
    <input ref="file-input-ref" type="file" accept="image/*" class="hidden" @change="onFileChange">

    <dialog ref="modal-ref" class="modal">
        <div class="modal-box transition-none">
            <button @click="modalRef.close()" class="btn btn-circle btn-sm btn-ghost absolute right-2 top-2">✕</button>
            <!-- 定义croppie绑定的标签 -->
            <div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>

            <div class="modal-action">
                <button @click="modalRef.close()" class="btn">Cancel</button>
                <button @click="crop" class="btn btn-neutral">Confirm</button>
            </div>
        </div>
    </dialog>

</template>

<style scoped>

</style>