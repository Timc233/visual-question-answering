<template>
  <div class="photo">
    <!--canvas截取流-->
    <!-- <img  ref="img" src="" alt="" style="width:640px; height:480px" crossorigin="anonymous"> -->
    <canvas ref="canvas" width="320" height="240"></canvas>
    <!--图片展示-->
    <video
      ref="video"
      width="320"
      height="240"
      autoplay
      crossorigin="anonymous"
    >
      <source src="http://127.0.0.1:5173" />
    </video>
    <!--确认-->
    <div class="buttons">
      <button @click="callCamera">ooemCamera</button>
      <button @click="closeCamera">close camera</button>
      <button @click="photograph">take photo</button>
    </div>
  </div>
</template>
<script setup>
import { reactive, ref } from "vue";
const video = ref(null);
const canvas = ref(null);
const img = ref(null);
const data = reactive({
  headImgSrc: "",
  dialogCamera: false,
});
// 调用摄像头
const callCamera = () => {
  // H5调用电脑摄像头API
  navigator.mediaDevices
    .getUserMedia({
      video: true,
    })
    .then((success) => {
      // 摄像头开启成功
      video.value.srcObject = success;
      // 实时拍照效果
      video.value.play();
    })
    .catch((error) => {
      console.error("摄像头开启失败，请检查摄像头是否可用！");
    });
};
// 拍照
const photograph = () => {
  let ctx = canvas.value.getContext("2d");
  // 把当前视频帧内容渲染到canvas上
  ctx.drawImage(video.value, 0, 0, 320, 240);
  // 转base64格式、图片格式转换、图片质量压缩
  let imgBase64 = canvas.value.toDataURL("image/jpg", 0.7); // 由字节转换为KB 判断大小

  let str = imgBase64.replace("data:image/jpeg;base64,", "");
  let strLength = str.length;
  let fileLength = parseInt(strLength - (strLength / 8) * 2); // 图片尺寸  用于判断
  let size = (fileLength / 1024).toFixed(2);
  console.log(size); // 上传拍照信息  调用接口上传图片 .........

  // 保存到本地
  console.log(data.dialogCamera);
  data.dialogCamera = false;
  let aTag = document.createElement("a");
  aTag.href = imgBase64;
  aTag.download = new Date().getTime() + ".jpeg";
  aTag.click();
};

// 关闭摄像头
const closeCamera = () => {
  if (!video.value.srcObject) {
    data.dialogCamera = false;
    return;
  }
  let stream = video.value.srcObject;
  let tracks = stream.getTracks();
  tracks.forEach((track) => {
    track.stop();
  });
  video.value.srcObject = null;
};
// 压缩图片 and 旋转角度纠正
const compressImage = (event) => {
  let _this = this;
  let file = event.target.files[0];
  let fileReader = new FileReader();
  let img = new Image();
  let imgWidth = "";
  let imgHeight = "";
  // 旋转角度
  let Orientation = null;
  // 缩放图片需要的canvas
  let canvas = document.createElement("canvas");
  let ctx = canvas.getContext("2d"); // 图片大小  大于2MB 则压缩
  const isLt2MB = file.size < 2097152;
  // 通过 EXIF 获取旋转角度 1 为正常  3 为 180°  6 顺时针90°  9 为 逆时针90°
  EXIF.getData(file, function () {
    EXIF.getAllTags(this);
    Orientation = EXIF.getTag(this, "Orientation");
  });
  // 文件读取 成功执行
  fileReader.onload = function (ev) {
    // 文件base64化，以便获知图片原始尺寸
    img.src = ev.target.result;
  };
  // 读取文件
  fileReader.readAsDataURL(file);
  // base64地址图片加载完毕后
  img.onload = function () {
    imgWidth = img.width;
    imgHeight = img.height;
    canvas.width = img.width;
    canvas.height = img.height;
    // 目标尺寸
    let targetWidth = imgWidth;
    let targetHeight = imgHeight;
    // 不需要压缩 不需要做旋转处理
    if (isLt2MB && imgWidth < 960 && imgHeight < 960 && !Orientation)
      return _this.XMLHttpRequest(file);
    if (isLt2MB && imgWidth < 960 && imgHeight < 960 && +Orientation === 1)
      return _this.XMLHttpRequest(file);
    // 大于2MB 、img宽高 > 960 则进行压缩
    if (!isLt2MB || imgWidth >= 960 || imgHeight >= 960) {
      // 最大尺寸
      let maxWidth = 850;
      let maxHeight = 850;
      // 图片尺寸超过 960 X 960 的限制
      if (imgWidth > maxWidth || imgHeight > maxHeight) {
        if (imgWidth / imgHeight > maxWidth / maxHeight) {
          // 更宽，按照宽度限定尺寸
          targetWidth = maxWidth;
          targetHeight = Math.round(maxWidth * (imgHeight / imgWidth));
        } else {
          targetHeight = maxHeight;
          targetWidth = Math.round(maxHeight * (imgWidth / imgHeight));
        }
      }
      // canvas对图片进行缩放
      canvas.width = targetWidth;
      canvas.height = targetHeight;
      // 图片大小超过 2Mb 但未旋转  则只需要进行图片压缩
      if (!Orientation || +Orientation === 1) {
        ctx.drawImage(img, 0, 0, targetWidth, targetHeight);
      }
    }
    // 拍照旋转 需矫正图片
    if (Orientation && +Orientation !== 1) {
      switch (+Orientation) {
        case 6: // 旋转90度
          canvas.width = targetHeight;
          canvas.height = targetWidth;
          ctx.rotate(Math.PI / 2);
          // 图片渲染
          ctx.drawImage(img, 0, -targetHeight, targetWidth, targetHeight);
          break;
        case 3: // 旋转180度
          ctx.rotate(Math.PI);
          // 图片渲染
          ctx.drawImage(
            img,
            -targetWidth,
            -targetHeight,
            targetWidth,
            targetHeight
          );
          break;
        case 8: // 旋转-90度
          canvas.width = targetHeight;
          canvas.height = targetWidth;
          ctx.rotate((3 * Math.PI) / 2);
          // 图片渲染
          ctx.drawImage(img, -targetWidth, 0, targetWidth, targetHeight);
          break;
      }
    } // 调用接口上传
    // base64 格式   我这是vuex 形式 重点是 canvas.toDataURL('image/jpeg', 1)
    // _this.$store.commit('SAVE_FACE_IMAGE_BASE64', canvas.toDataURL('image/jpeg', 1))
    // _this.upAppUserFaceByBase64()
    // 通过文件流格式上传
    canvas.toBlob(
      function (blob) {
        _this.XMLHttpRequest(blob);
      },
      "image/jpeg",
      1
    );
  };
};
// 上传base64方式
const upAppUserFaceByBase64 = () => {
  this.$store
    .dispatch("upAppUserFaceByBase64", {
      baseFace: this.$store.state.faceImageBase64,
    })
    .then((res) => {
      // 上传成功
    })
    .catch((err) => {
      console.log(err);
    });
};
// 上传
const XMLHttpRequest = (params) => {
  // 图片ajax上传
  let action = "后台接口地址";
  let xhr = new XMLHttpRequest();
  let formData = new FormData();
  formData.delete("multipartFile");
  formData.append("multipartFile", params);
  // 文件上传成功回调
  xhr.onprogress = this.updateProgress;
  xhr.onerror = this.updateError;
  // 开始上传
  xhr.open("POST", action, true);
  xhr.send(formData);
};
// 上传成功回调
const updateProgress = (res) => {
  // res 就是成功后的返回
};
// 上传失败回调
const updateError = (error) => {
  console.log(error);
};
</script>
<style scoped lang="less">
.photo {
  .buttons {
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>
