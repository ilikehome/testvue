/// <reference types="vite/client" />
// 新增：声明.vue文件的类型，让TypeScript能识别Vue组件
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}