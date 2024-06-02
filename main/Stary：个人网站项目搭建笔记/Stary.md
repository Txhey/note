# Stary

## 功能设计

整体功能可总结为以下：

* 主页
* 博客
* 项目
* 个人介绍



### 博客

实体属性：

| param                  | name           | description                                                  |
| ---------------------- | -------------- | ------------------------------------------------------------ |
| id                     | id             | 唯一表示                                                     |
| author (暂不用)        | 作者           | 一般个人网站的作者都是自己，但保不齐以后有什么其他功能（保留） |
| title                  | 标题           |                                                              |
| content                | 内容           |                                                              |
| index_content (暂不用) | 索引内容       | 各级标题的集合，用于快速索引查询内容                         |
| tag                    | 标签           | 用于索引                                                     |
| create_time            | 创建时间       |                                                              |
| last_modify            | 上一次修改时间 |                                                              |
| img                    | 封面图片地址   |                                                              |

功能：

* [添加博客](#添加博客)
* 删除博客
* 修改博客
* 查询博客



**添加博客**



## 页面设计

* index
  * home
  * blog
  * project
  * plan
  * me
* blogEditor（不要了）
* blogView



## 后端设计

上传图片

```java
// 上传图片返回地址，如果name为空，则为file.name
public String uploadImg(MultipartFile file,int noteId, String name);
```



## 实现

### Vue

#### 创建项目

```bash
# 创建vite项目
npm create vite@latest blog-vue3-1.0.2

cd blog-vue3-1.0.2
npm install
npm run dev
```

#### 

#### 第三方组件

* router (路由)
* vite-plugin-svg-icons (svg自定义颜色和大小)
* element-plus (组件库)
* md-editor-v3 (markdown编辑器组件)
* mitt (组件之间通信)
* sass (css更清晰的写法标准)
* axios (HTTP访问服务端)

```bash
npm add vue-router@4

npm add fast-glob
npm add vite-plugin-svg-icons

npm add element-plus

npm add md-editor-v3

npm add mitt

npm add sass

npm add axios

npm install pinia
```



#### 配置

##### `vite.config.js`

* 配置vite-plugin-svg-icons库的配置内容
  * 图标文件夹
  * symbolId格式
* 路径转化
  * 将src的地址映射给@符号

```js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import { createSvgIconsPlugin } from 'vite-plugin-svg-icons'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue(),
        createSvgIconsPlugin({
            // 指定需要缓存的图标文件夹
            iconDirs: [path.resolve(process.cwd(), 'src/assets/svg')],
            // 指定symbolId格式
            symbolId: 'icon-[name]',
        })
    ],
    // 路径转化
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src/'),
        }
    }
})
```



##### 路由路径

src / router / `index.js`

```js
import { createWebHistory, createRouter } from "vue-router";

import Index from '@/components/index/Index.vue'
import Blog from '@/components/index/blog/Blog.vue'
import Me from "@/components/index/me/Me.vue"

// me的子组件
import Profile from '@/components/index/me/module/Profile.vue'

import BlogEditor from "@/components/blogEditor/BlogEditor.vue";

const routes = [
    {
        path: "/",
        redirect: "/index/home"
    },
    {
        path: "/index",
        name: "Index",
        component: Index,
        children: [
            {
                path: "blog",
                name: Blog,
                component: Blog
            },
            {
                path: "me",
                name: Me,
                component: Me,
                redirect: "/index/me/profile",
                children: [
                    {
                        path: "profile",
                        name: Profile,
                        component: Profile
                    }
                ]
            },
        ]
    },
    {
        path: "/blogEditor",
        component: BlogEditor
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
```



##### `index.html`

修改title内容

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <!-- 修改title内容 -->
    <title>Stary</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>

```

##### 跨域问题

在`main.js`中设置axios的默认配置，添加`withCredentials`配置

```js
import axios from 'axios'
// 全局设置基础 URL
axios.defaults.baseURL = 'http://localhost:8080';
axios.defaults.withCredentials = ture;
```





### SpringBoot

#### 创建空项目

#### 跨域问题

服务器端新建 config/`WebConfig.java` 配置跨域配置

```java
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CORSConfig implements WebMvcConfigurer {

    public void addCorsMappings(CorsRegistry registry) {
        // 设置允许跨域的路径
        registry.addMapping("/**")
            // 设置允许跨域请求的域名
            .allowedOriginPatterns("*")
            // 是否允许cookie
            .allowCredentials(true)
            // 设置允许的请求方式
            .allowedMethods("GET", "POST", "DELETE", "PUT")
            // 设置允许的header属性
            .allowedHeaders("*")
            // 跨域允许时间
            .maxAge(3600);
    }
}
```
