<template>
    <div class="recorder">
      <div>
        <Button type="success" @click="getPermission()">get recorder permission</Button>
  
        <Button type="info" @click="onPlay()">start to record</Button>
  
        <Button type="info" @click="resumeRecorder()">continue recording</Button>
  
        <Button type="info" @click="pauseRecorder()">pause recording</Button>
  
        <Button type="info" @click="stopRecorder()">end recording</Button>
      </div>
  
      <div>
        <Button type="success" @click="playRecorder()">display voice</Button>
  
        <Button type="success" @click="pausePlayRecorder()">pause display</Button>
  
        <Button type="success" @click="resumePlayRecorder()">resume display</Button>
  
        <Button type="success" @click="stopPlayRecorder()">pause display</Button>
      </div>
  
      <div>
        <Button type="info" @click="getRecorder()">get record information</Button>
  
        
  
        <!-- <Button type="info" @click="downWAV()">downloadWAV</Button> -->
  
        <Button type="info" @click="getMp3Data()">downloadMP3</Button>
  
        <Button type="error" @click="destroyRecorder()">delete</Button>
         <!--音频-->
         <audio v-show="false"
               ref="audioRef"
               class="bgMusic"
               controls
               :autoplay="false"
               style="display: none"
               @ended="overAudio"
               @pause="onPause"
               @play="onPlay"
        >
            <source src="../../assets/mp3/ttsMP3.com_VoiceText_2022-11-27_0_0_41.mp3" type="audio/mpeg">
        </audio>

      </div>
    </div>
  </template>
  
  <script setup>
  import Recorder from "js-audio-recorder";
  import lamejs from "lamejs";
  import { ref } from "vue";

  const recorder = new Recorder({
    sampleBits: 16, // 采样位数，支持 8 或 16，默认是16
  
    sampleRate: 48000, // 采样率，支持 11025、16000、22050、24000、44100、48000
  
    numChannels: 1, // 声道，支持 1 或 2， 默认是1
  
    // compiling: false,(0.x版本中生效,1.x增加中) // 是否边录边转换，默认是false
  });
  
  // 播放录音提示
/**
 * audio自身事件
 * */
// 当音频播放
const audioRef = ref()
const  onPlay = () => {
  console.log('开始播放声音');
  console.log(audioRef)
  audioRef.value.play()
}
// 当音频暂停
const onPause = () => {
  console.log('暂停播放声音');
  audioRef.value.pause()
}
//播放完毕执行
const overAudio =() => { 
  console.log('播放声音完毕');
  // this.audioArr.forEach(item=>{
  //     item.isStart = true;
  // })
  startRecorder();
}

  
  // 绑定事件-打印的是当前录音数据
  
  //recorder.onprogress = function (params) {
  // console.log('--------------START---------------')
  // console.log('录音时长(秒)', params.duration);
  // console.log('录音大小(字节)', params.fileSize);
  // console.log('录音音量百分比(%)', params.vol);
  // console.log('当前录音的总数据([DataView, DataView...])', params.data);
  // console.log('--------------END---------------')
  //};
  
  name: "recorder";
  
  /**
  
    * 录音的具体操作功能
  
    * */
  
  // 开始录音
  
   const startRecorder = () => {
    recorder.start().then(
      () => {},
      (error) => {
        // 出错了
  
        console.log(`${error.name} : ${error.message}`);
      }
    );
  };
  
  // 继续录音
  
  const resumeRecorder = () => {
    recorder.resume();
  };
  
  // 暂停录音
  
  const pauseRecorder = () => {
    recorder.pause();
  };
  
  // 结束录音
  
  const stopRecorder = () => {
    recorder.stop();
  };
  
  // 录音播放
  
  const playRecorder = () => {
    recorder.play();
  };
  
  // 暂停录音播放
  
  const pausePlayRecorder = () => {
    recorder.pausePlay();
  };
  
  // 恢复录音播放
  
  const resumePlayRecorder = () => {
    recorder.resumePlay();
  };
  
  // 停止录音播放
  
  const stopPlayRecorder = () => {
    recorder.stopPlay();
  };
  
  // 销毁录音
  
  const destroyRecorder = () => {
    recorder.destroy().then(function () {
      recorder = null;
    });
  };
  
  /**
  
    * 获取录音文件
  
    * */
  
  const getRecorder = () => {
    let toltime = recorder.duration; //录音总时长
  
    let fileSize = recorder.fileSize; //录音总大小
  
    //录音结束，获取取录音数据
  
    let PCMBlob = recorder.getPCMBlob(); //获取 PCM 数据
  
    let wav = recorder.getWAVBlob(); //获取 WAV 数据
  
    let channel = recorder.getChannelData(); //获取左声道和右声道音频数据
  
    debugger;
  };
  
  /**
  
    * 下载录音文件
  
    * */
  
  //下载pcm
  
  const downPCM = () => {
    //这里传参进去的时文件名
  
    recorder.downloadPCM("新文件");
  };
  
  //下载wav
  
  const downWAV = () => {
    //这里传参进去的时文件名
  
    recorder.downloadWAV("新文件");
  };
  
  /**
  
    * 获取麦克风权限
  
    * */
  
  const getPermission = () => {
    Recorder.getPermission().then(
      () => {
        this.$Message.success("获取权限成功");
      },
      (error) => {
        console.log(`${error.name} : ${error.message}`);
      }
    );
  };
  
  /**
  
    * 文件格式转换 wav-map3
  
    * */
  
  const getMp3Data = () => {
    const mp3Blob = convertToMp3(recorder.getWAV());
  
    recorder.download(mp3Blob, "recorder", "mp3");
  };
  
  const convertToMp3 = (wavDataView) => {
    // 获取wav头信息
  
    const wav = lamejs.WavHeader.readHeader(wavDataView); // 此处其实可以不用去读wav头信息，毕竟有对应的config配置
  
    const { channels, sampleRate } = wav;
  
    const mp3enc = new lamejs.Mp3Encoder(channels, sampleRate, 128);
  
    // 获取左右通道数据
  
    const result = recorder.getChannelData();
  
    const buffer = [];
  
    const leftData =
      result.left &&
      new Int16Array(result.left.buffer, 0, result.left.byteLength / 2);
  
    const rightData =
      result.right &&
      new Int16Array(result.right.buffer, 0, result.right.byteLength / 2);
  
    const remaining = leftData.length + (rightData ? rightData.length : 0);
  
    const maxSamples = 1152;
  
    for (let i = 0; i < remaining; i += maxSamples) {
      const left = leftData.subarray(i, i + maxSamples);
  
      let right = null;
  
      let mp3buf = null;
  
      if (channels === 2) {
        right = rightData.subarray(i, i + maxSamples);
  
        mp3buf = mp3enc.encodeBuffer(left, right);
      } else {
        mp3buf = mp3enc.encodeBuffer(left);
      }
  
      if (mp3buf.length > 0) {
        buffer.push(mp3buf);
      }
    }
  
    const enc = mp3enc.flush();
  
    if (enc.length > 0) {
      buffer.push(enc);
    }
  
    return new Blob(buffer, { type: "audio/mp3" });
  };
  </script>
  
  <style lang="less" scoped>
  .recorder {
    display: flex;
    justify-content: center;
    // flex-direction: column;
    Button{
      margin: 1vh;
      width: 106px;
    }
  }
  </style>
  