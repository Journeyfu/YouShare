/*
 * 功能：在每个请求头里自动添加`access token`。
 * 然后拦截请求结果，如果返回结果是身份认证失败（401），
 * 则说明`access_token`过期了，
 * 那么先用`cookie`中的`refresh_token`刷新`access_token`。
 * 如果刷新失败则说明`refreh_token`也过期了，
 * 则调用`user.logout()`在浏览器内存中删除登录状态；
 * 如果刷新成功，则重新发送原请求。
*/

import axios from "axios"
import {useUserStore} from "@/stores/user.js";

const BASE_URL = 'http://127.0.0.1:8000'

const api = axios.create({
    baseURL: BASE_URL,
    withCredentials: true, // 允许浏览器在跨域请求时，携带并接收“凭证”
})
// 拦截器, 错误响应可以忽略，这里拦截器的作用就是判断当前是否存在access token，
api.interceptors.request.use(config => {
    const user = useUserStore()
    if (user.accessToken) {
        // Bearer = “我带着令牌来访问资源” 的标准用法
        config.headers.Authorization = `Bearer ${user.accessToken}`
    }
    return config
})

let isRefreshing = false
let refreshSubscribers = []

function subscribeTokenRefresh(callback) {
    refreshSubscribers.push(callback)
}

function onRefreshed(token) {
    refreshSubscribers.forEach(cb => cb(token))
    refreshSubscribers = []
}

function onRefreshFailed(err) {
    refreshSubscribers.forEach(cb => cb(null, err))
    refreshSubscribers = []
}

// 这些事情默认都发生在：同一个浏览器、同一个页面（同一个 JS 运行上下文）里
api.interceptors.response.use(
    response => response,
    async error => { // 这里的async并没有在后面跟await配合，所以这里只是充当个接口作用
        const user = useUserStore()
        // ?.config：保证“error 不存在时不会报错”，不是保证 config一定存在 -- 确保的是 对象本身不存在的时候 不会报错
        // 即： 如果error存在，而config不存在的时候， 不会报错，会返回undefined
        // 下面三行代码是一块使用的
        const originalRequest = error?.config
        if (!originalRequest) {
            return Promise.reject(error)
        }
        // originalRequest如果不存在_retry, 则会返回undefined,  !undefined === true成立
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            return new Promise((resolve, reject) => { // 获得resolve和reject,两个函数，用来决定这个响应是否成功
                // subscribeTokenRefresh 只负责 把 callback 存起来
                // 在OnRefreshed 和 OnRefreshFailed 的时候才会调用

                subscribeTokenRefresh((token, error) => {
                    if (error) {
                        reject(error)
                    } else {
                        originalRequest.headers.Authorization = `Bearer ${token}`
                        resolve(api(originalRequest))
                    }
                })

                if (!isRefreshing) { // 如果没有刷新过，则再刷新一次
                    isRefreshing = true
                    axios.post( // 全局post， 不会受到实例拦截器影响
                        `${BASE_URL}/api/user/account/refresh_token/`,
                        {},
                        {withCredentials: true, timeout: 5000}
                    ).then(res => { // 成功分支 “刷新”的结果就是拿到一个新的 access token
                        user.setAccessToken(res.data.access)
                        onRefreshed(res.data.access)
                    }).catch(error => { // 失败分支 ，用户需要重新登录
                        user.logout()
                        onRefreshFailed(error)
                        reject(error)
                    }).finally(() => { // 最后都进入这里
                        isRefreshing = false
                    })
                }
            })
        }

        return Promise.reject(error)
    }
)

export default api