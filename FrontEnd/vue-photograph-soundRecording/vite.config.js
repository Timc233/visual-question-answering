import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

/************************************* 路径配置 start ********************************/
import { resolve } from 'path' 

const pathResolve = (dir) => {  
  return resolve(__dirname, ".", dir)          
}

const alias = {
  '@': pathResolve("src")
}
/************************************* 路径配置 end ********************************/
// https://vitejs.dev/config/
export default defineConfig({
  base:'./',
  plugins: [vue()],
  resolve: {  // ****************** 路径配置新增
    alias     // ****************** 路径配置新增
  }           // ****************** 路径配置新增
})
