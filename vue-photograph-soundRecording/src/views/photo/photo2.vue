<template>
  <div>
    <button type="primary" @click="openVideo">openVedio</button>
    <button @click="closeVideo">closeVedio</button>
    <button type="danger" @click="screenshot">screenshot</button>
    <div>
      <video id="video" ref="videoRef" />
    </div>
    <canvas ref="canvasRef" width="400" height="300" style="display: none" />
    <!-- 截图展示图片 -->
    <img ref="screenshotRef" />
  </div>
</template>

<script setup>
import { ref } from "vue";
// 获取canvas
const canvasRef = ref(null);
// 获取视频
const videoRef = ref(null);
 // 获取截图的地址
const screenshotRef = ref(null);

// 打开摄像头
const openVideo = () => {
 
  console.log("navigator.mediaDevices", navigator.mediaDevices);
  if (navigator.mediaDevices === undefined) {
    navigator.mediaDevices = {};
  }
 
  if (navigator.mediaDevices.getUserMedia === undefined) {
    navigator.mediaDevices.getUserMedia = (constraints) => {
     
      const getUserMedia =
        navigator.getUserMedia ||
        (navigator.getUserMedia =
          navigator.mozGetUserMedia ||
          navigator.webkitGetUserMedia ||
          navigator.msGetUserMedia);
      console.log("getUserMedia", getUserMedia);
    
      if (!getUserMedia) {
        return Promise.reject(new Error("该浏览器暂不支持摄像头！"));
      }
     
      return new Promise((resolve, reject) => {
        getUserMedia.call(navigator, constraints, resolve, reject);
      });
    };
  }
  const constraints = {
    audio: true,
    video: {
      width: { ideal: 320, max: 640 },
      height: { ideal: 240, max: 480 },
    },
  };
  console.log("window.navigator", window.navigator);
  window.navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      // 旧的浏览器可能没有srcObject
      if ("srcObject" in video) {
        videoRef.value.srcObject = stream;
      } else {
        // 防止在新的浏览器里使用它，因为它已经不再支持了
        videoRef.value.video.src = window.URL.createObjectURL(stream);
      }
      video.onloadedmetadata = (e) => {
        video.play();
      };
    })
    .catch((err) => {
      console.log(err.name + ": " + err.message);
    });
};
// 截图
const screenshot = () => {
  // 渲染一个2d平面的视图
  const ctx = canvasRef.value.getContext("2d");
  // 设置canvas 视图文件地址和大小
  ctx.drawImage(videoRef.value, 0, 0, 400, 300);
  // 将数据转为base64赋值给img标签的src属性
  screenshotRef.value.src = canvasRef.value.toDataURL("image/png");
  console.log("screenshot.src", screenshotRef.value.src);
  const imgData = canvas
    .toDataURL("image/png")
    .replace("image/png", "image/octet-stream");
  // 下载图片到本地
  const save_link = document.createElementNS(
    "http://www.w3.org/1999/xhtml",
    "a"
  );
  save_link.href = imgData;
  save_link.download = "file_" + new Date().getTime() + ".png";
  save_link.click();
};
// 关闭摄像头
const closeVideo = () => {
  console.log("srcObject", videoRef.value.srcObject);
  const srcObject = videoRef.value.srcObject
    ? videoRef.value.srcObject.getTracks()
    : videoRef.value.src.getTracks();
  srcObject.forEach((track) => {
    track.stop();
    videoRef.value.src = null;
  });
};
</script>

<style lang="less" scoped></style>
