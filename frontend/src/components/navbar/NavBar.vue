<script setup>

import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import {useUserStore} from "@/stores/user.js";
import UserMenu from "@/components/navbar/UserMenu.vue";

const user = useUserStore()
</script>

<template>
    <!-- copied from https://daisyui.com/components/drawer/ -->
    <div class="drawer lg:drawer-open">
        <input id="my-drawer-4" type="checkbox" class="drawer-toggle"/>
        <div class="drawer-content">
            <!-- Navbar -->
            <nav class="navbar w-full bg-base-100 shadow-sm">
                <div class="navbar-start">
                    <label for="my-drawer-4" aria-label="open sidebar" class="btn btn-square btn-ghost">
                        <MenuIcon />
                    </label>
                    <div class="px-2 font-bold text-xl">AI Friends</div>
                </div>
                <div class="narbar-center w-4/5 max-w-180 flex justify-center">
                    <div class="join w-4/5 flex justify-center">
                      <input class="input join-item rounded-l-full w-4/5" placeholder="Search everything you interest" />
                      <button class="btn join-item rounded-r-full">
                          <SearchIcon />
                          Search
                      </button>
                    </div>
                </div>
                <div class="navbar-end">
                    <RouterLink v-if="user.isLogin()" active-class="btn-active"  :to="{name: 'create-index'}" class="btn btn-ghost text-base mr-6">
                        <CreateIcon />
                        Creation
                    </RouterLink>
                    <RouterLink v-if="user.hasPulledUserInfo && !user.isLogin()" :to="{name: 'user-account-login-index'}" active-class="btn-active" class="btn btn-ghost text-lg">
                        Login
                    </RouterLink>
                    <UserMenu v-else-if="user.isLogin()" />
                </div>

            </nav>
            <!-- Page content here -->
            <!-- <slot> 是 Vue 组件里的“占位符”，用来让父组件把内容传进子组件里渲染 -->
            <slot>  </slot>
        </div>

        <div class="drawer-side is-drawer-close:overflow-visible">
            <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>
            <div class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-16 is-drawer-open:w-54">
                <!-- Sidebar content here -->
                <ul class="menu w-full grow">
                    <!-- List item -->
                    <li>
                        <RouterLink :to="{name: 'homepage-index'}"  active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Homepage">
                            <!-- Home icon -->
                            <HomepageIcon />
                            <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Homepage</span>
                        </RouterLink>
                    </li>

                    <li>
                        <RouterLink :to="{name: 'friend-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Friend">
                            <FriendIcon />
                            <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Friend</span>
                        </RouterLink>
                    </li>

                    <li>
                        <RouterLink :to="{name: 'create-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="Creation">
                            <CreateIcon />
                            <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">Creation</span>
                        </RouterLink>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>