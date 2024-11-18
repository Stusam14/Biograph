<script lang="ts" setup>
    import { defineComponent } from 'vue';
    import UilFileUpload from './icons/UilFileUpload.vue';
    import {ref , computed} from 'vue';
    import { uploadFiles } from '@/api/api';
    
    defineComponent({
        name: "file-upload",
        components: {
            UilFileUpload,
        }
    });

    const files = ref<File[]>([]);
    // const fileInput = ref<HTMLElement | null>(null);
    const disabled = computed(()=> files.value.length === 0);

    const onFileChange = (event: Event) : void => {
        const input = event.target as HTMLInputElement
        const fileList : FileList | null = input.files;
        if (fileList) {
            files.value = Array.from(fileList);
        }
    }

    const handleFileChange = (event: Event) : void => {
    };

    const handleDrop = (event: Event) : void => {}

    const onSubmit = async () : Promise<void> => {
        try{
            await uploadFiles(files.value) ;
            // clear the file input 
            files.value = []
        } catch(error) {
            // TODO : <Error/> to render 
        }
    };
    
</script>

<template>
    <slot name="header"></slot>

    <div class="upload-container">
        <label for="file-input">
            <span>Choose file</span>
            <input type="file" id="file-input" @change="handleFileChange" />
        </label>
        <div class="drop-zone" @drop="handleDrop" @dragover.prevent>
            Drag and drop file here
        </div>
    </div>
    <form method="post" enctype="multipart/form-data" 
        @submit.prevent="onSubmit" 
        @change="onFileChange" >

        <input type="file" accept=".xml" multiple>
        <button type="submit" :disabled>
            <span class="button__icon">
                <uil-file-upload></uil-file-upload>
            </span>
            <span class="button__text">Convert</span>
        </button>

    </form>
</template>

<style scoped>
    form button[type = "submit"] {
        margin: 0 auto;
        display: flex;
        height: 50px;
        padding: 0;
        background: #009578;
        border: none;
        outline: none;
        border-radius: 5px;
        overflow: hidden;
        font-family:"Quicksand" sans-serif ;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
    }

    form button[type = "submit"]:hover {
        background-color: #008168;
    }

    form button[type="submit"]:active {
        background-color: #006e58;
    }

    form input[type=button] {
        background-color: aquamarine;
    }

    .button__text, .button__icon {
        display: inline-flex;
        align-items: center;
        padding: 0 12px;
        color: #fff;
        height: 100%;
    }

    .box {
        width: 500px;
        height: 500px;
        border: 1px dotted rgb(151, 144, 144);
        position: relative;
    } 

    .upload-container {
        text-align: center;
    }

    .upload-container label {
         display: inline-block;
        padding: 10px;
        border: 1px solid #ccc;
        cursor: pointer;
    }

    .upload-container input[type="file"] {
        display: none;
    }

    .upload-container .drop-zone {
        border: 2px dashed #ccc;
        padding: 20px;
        text-align: center;
        cursor: pointer;
    }

</style>
