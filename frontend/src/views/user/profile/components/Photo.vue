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

// 用户选择或点击头像 → openModal(photo)
// 弹窗出现
// Croppie 初始化
// 图片绑定到 Croppie
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

// 用户拖动、缩放、裁剪图片 → 点击确认 → crop()
// 获取裁剪后的 base64 图片
// 更新头像显示
// 关闭弹窗
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
    // FileReader 是 浏览器自带的 API，用来读取文件（File 或 Blob）的内容
    const reader = new FileReader()
    // reader.result 就是读取到的文件内容
    // 调用 openModal(reader.result)： 也就是把这个文件的数据传给你之前写的 Croppie 裁剪弹窗
    reader.onload = () =>{
        openModal(reader.result)
    }

    //  把文件读取成 base64 数据 URL。读取完成后会触发 onload 回调。这个 base64 URL 就可以直接赋给 <img src="..."> 或 Croppie 来显示图
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
            <!--  fileInputRef 对应的是一个input控件，所以有input函数           -->
            <!--  调用 fileInputRef.click() 会打开文件选择对话框。          -->
            <div @click="fileInputRef.click()" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
                <!--  头像上渲染个相机   -->
                <CameraIcon />
            </div>
        </div>
    </div>
    <!-- 选择文件后，会触发onFileChange   -->
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